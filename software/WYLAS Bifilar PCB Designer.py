import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math

# Bifilar / planar spiral DXF layout tool
# No external Python packages required. Writes ASCII DXF R12 polylines.
# Supports smooth circular spirals and lightweight polygon spirals.


class Coil:
    def __init__(self, name, inner_d=4.5, pitch=0.75, turns=6.0,
                 copper=0.5, gap=0.25, direction='CCW',
                 geometry='Circular', polygon_sides=8, trim_start=0,
                 x=None, y=None):
        self.name = name
        self.inner_d = float(inner_d)
        self.pitch = float(pitch)
        self.turns = float(turns)
        self.copper = float(copper)
        self.gap = float(gap)
        self.direction = direction
        self.geometry = geometry
        self.polygon_sides = int(polygon_sides)
        self.trim_start = int(trim_start)
        self.x = x
        self.y = y

    @property
    def inner_r(self):
        return self.inner_d / 2.0

    @property
    def outer_r_centerline(self):
        """Nominal radial centerline distance measured to the side/apothem."""
        return self.inner_r + self.pitch * self.turns

    @property
    def polygon_radius_factor(self):
        """Convert polygon apothem to vertex radius."""
        if self.geometry == 'Polygon' and self.polygon_sides >= 3:
            return 1.0 / math.cos(math.pi / self.polygon_sides)
        return 1.0

    @property
    def max_centerline_radius(self):
        return self.outer_r_centerline * self.polygon_radius_factor


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WYLAS Bifilar PCB Designer - V1 PCB to Fusion 360 Script for automation')
        self.geometry('1220x790')
        self.minsize(1040, 680)
        self.coils = []
        self.selected = None
        self._build_ui()
        self.load_tesla_defaults()

    def _build_ui(self):
        root = ttk.Frame(self, padding=8)
        root.pack(fill='both', expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # Scrollable left-side options panel.
        controls_shell = ttk.Frame(root)
        controls_shell.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        controls_shell.rowconfigure(0, weight=1)
        controls_shell.columnconfigure(0, weight=1)

        controls_canvas = tk.Canvas(
            controls_shell, width=335, highlightthickness=0, borderwidth=0
        )
        controls_scroll = ttk.Scrollbar(
            controls_shell, orient='vertical',
            command=controls_canvas.yview
        )
        controls_canvas.configure(yscrollcommand=controls_scroll.set)
        controls_canvas.grid(row=0, column=0, sticky='nsew')
        controls_scroll.grid(row=0, column=1, sticky='ns')

        controls = ttk.Frame(controls_canvas)
        controls_window = controls_canvas.create_window(
            (0, 0), window=controls, anchor='nw'
        )

        def update_scrollregion(event=None):
            controls_canvas.configure(scrollregion=controls_canvas.bbox('all'))

        def fit_controls_width(event):
            controls_canvas.itemconfigure(controls_window, width=event.width)

        controls.bind('<Configure>', update_scrollregion)
        controls_canvas.bind('<Configure>', fit_controls_width)

        def controls_mousewheel(event):
            if getattr(event, 'num', None) == 4:
                controls_canvas.yview_scroll(-3, 'units')
            elif getattr(event, 'num', None) == 5:
                controls_canvas.yview_scroll(3, 'units')
            else:
                delta = getattr(event, 'delta', 0)
                if delta:
                    controls_canvas.yview_scroll(
                        int(-delta / 120) * 3, 'units'
                    )
            return 'break'

        # Bind the wheel only while the pointer is over the left panel.
        def bind_wheel(event=None):
            controls_canvas.bind_all('<MouseWheel>', controls_mousewheel)
            controls_canvas.bind_all('<Button-4>', controls_mousewheel)
            controls_canvas.bind_all('<Button-5>', controls_mousewheel)

        def unbind_wheel(event=None):
            controls_canvas.unbind_all('<MouseWheel>')
            controls_canvas.unbind_all('<Button-4>')
            controls_canvas.unbind_all('<Button-5>')

        controls_canvas.bind('<Enter>', bind_wheel)
        controls_canvas.bind('<Leave>', unbind_wheel)
        controls.bind('<Enter>', bind_wheel)
        controls.bind('<Leave>', unbind_wheel)

        preview_frame = ttk.Frame(root)
        preview_frame.grid(row=0, column=1, sticky='nsew')
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        area = ttk.LabelFrame(controls, text='PCB / Coil Area (mm)', padding=8)
        area.pack(fill='x', pady=(0, 8))
        self.area_w = tk.StringVar(value='26')
        self.area_h = tk.StringVar(value='26')
        self._entry(area, 'Width', self.area_w, 0)
        self._entry(area, 'Height', self.area_h, 1)
        ttk.Button(area, text='Redraw Area', command=self.redraw).grid(
            row=2, column=0, columnspan=2, sticky='ew', pady=(6, 0)
        )

        editor = ttk.LabelFrame(controls, text='Coil Properties', padding=8)
        editor.pack(fill='x', pady=(0, 8))

        self.inner_d = tk.StringVar(value='4.5')
        self.pitch = tk.StringVar(value='0.75')
        self.turns = tk.StringVar(value='6')
        self.copper = tk.StringVar(value='0.50')
        self.gap = tk.StringVar(value='0.25')
        self.direction = tk.StringVar(value='CCW')
        self.geometry = tk.StringVar(value='Polygon')
        self.polygon_sides = tk.StringVar(value='8')
        self.trim_start = tk.StringVar(value='0')

        self._entry(editor, 'Inner diameter', self.inner_d, 0)
        self._entry(editor, 'Pitch', self.pitch, 1)
        self._entry(editor, 'Turns', self.turns, 2)
        self._entry(editor, 'Copper width', self.copper, 3)
        self._entry(editor, 'Gap', self.gap, 4)
        self._entry(editor, 'Trim start vertices', self.trim_start, 5)

        ttk.Label(editor, text='Direction').grid(row=6, column=0, sticky='w', pady=2)
        ttk.Combobox(
            editor, textvariable=self.direction,
            values=('CCW', 'CW'), state='readonly', width=12
        ).grid(row=6, column=1, sticky='ew', pady=2)

        ttk.Label(editor, text='Geometry').grid(row=7, column=0, sticky='w', pady=2)
        geom_box = ttk.Combobox(
            editor, textvariable=self.geometry,
            values=('Circular', 'Polygon'), state='readonly', width=12
        )
        geom_box.grid(row=7, column=1, sticky='ew', pady=2)
        geom_box.bind('<<ComboboxSelected>>', self.on_geometry_changed)

        self.sides_label = ttk.Label(editor, text='Polygon sides')
        self.sides_label.grid(row=8, column=0, sticky='w', pady=2)
        self.sides_entry = ttk.Entry(editor, textvariable=self.polygon_sides, width=13)
        self.sides_entry.grid(row=8, column=1, sticky='ew', pady=2)

        ttk.Label(
            editor,
            text='Pitch is centerline-to-centerline.\n'
                 'For polygons, inner diameter is the nominal\n'
                 'inscribed centerline diameter.',
            foreground='#555'
        ).grid(row=9, column=0, columnspan=2, sticky='w', pady=(5, 0))

        buttons = ttk.Frame(editor)
        buttons.grid(row=10, column=0, columnspan=2, sticky='ew', pady=(8, 0))
        buttons.columnconfigure((0, 1), weight=1)
        ttk.Button(buttons, text='Add Coil', command=self.add_coil).grid(
            row=0, column=0, sticky='ew', padx=(0, 3)
        )
        ttk.Button(buttons, text='Update Selected', command=self.update_selected).grid(
            row=0, column=1, sticky='ew', padx=(3, 0)
        )


        export = ttk.LabelFrame(controls, text='DXF', padding=8)
        export.pack(fill='x', pady=(0, 8))
        ttk.Button(
            export, text='Export DXF…', command=self.export_dxf
        ).pack(fill='x')
        ttk.Button(
            export, text='Export Fusion Single PCB Script…',
            command=self.export_fusion_script
        ).pack(fill='x', pady=(5, 0))

        tesla = ttk.LabelFrame(controls, text='Tesla Cell Pads / Nail', padding=8)
        tesla.pack(fill='x', pady=(0, 8))

        self.show_tesla = tk.BooleanVar(value=True)
        self.nail_d = tk.StringVar(value='5.0')
        self.nail_clearance = tk.StringVar(value='1.25')
        self.inner_pad_d = tk.StringVar(value='3.0')
        self.outer_pad_d = tk.StringVar(value='3.0')
        self.edge_clearance = tk.StringVar(value='1.25')
        self.pad_angle = tk.StringVar(value='45.0')
        self.bridge_pad_d = tk.StringVar(value='3.0')
        self.pad_drill_d = tk.StringVar(value='1.0')
        self.bridge_drill_d = tk.StringVar(value='1.0')
        self.duplicate_bottom = tk.BooleanVar(value=False)

        # Array V5: one large PCB, Top = coils, Bottom = series routing.
        self.array_cols = tk.StringVar(value='8')
        self.array_rows = tk.StringVar(value='8')
        self.array_route_width = tk.StringVar(value='3.0')
        self.array_top_mask_width = tk.StringVar(value='2.60')
        # ENTRY/EXIT terminal copper annular rim:
        # pad diameter = drill diameter + 2 * rim.
        # Default 1.25 mm rim with 1.00 mm drill = 3.50 mm terminal pad.
        self.array_terminal_rim = tk.StringVar(value='1.25')
        # ARRAY ONLY: extra edge-to-pad clearance measured from the local
        # cell corner to the edge of the round corner pad. 0.0 places the
        # pad tangent to the cell corner lines; the full PCB still retains
        # the master board-edge clearance outside the array grid.
        self.array_corner_pad_offset = tk.StringVar(value='0.25')

        ttk.Checkbutton(
            tesla, text='Show / export Tesla pads',
            variable=self.show_tesla, command=self.redraw
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 4))
        self._entry(tesla, 'Nail hole Ø', self.nail_d, 1)
        self._entry(tesla, 'Nail clearance (follows edge)', self.nail_clearance, 2)
        self._entry(tesla, 'Inner pad Ø', self.inner_pad_d, 3)
        self._entry(tesla, 'Outer pad Ø', self.outer_pad_d, 4)
        self._entry(tesla, 'Copper/pad edge clearance', self.edge_clearance, 5)
        self._entry(tesla, 'Inner pad angle °', self.pad_angle, 6)
        self._entry(tesla, 'NE bridge pad Ø', self.bridge_pad_d, 7)
        self._entry(tesla, 'Endpoint pad drill Ø', self.pad_drill_d, 8)
        self._entry(tesla, 'NE bridge drill Ø', self.bridge_drill_d, 9)

        ttk.Label(
            tesla,
            text='Final layer mode: Top = coils, Bottom = 3 mm routing',
            foreground='#555'
        ).grid(row=10, column=0, columnspan=2, sticky='w', pady=(6, 2))

        ttk.Button(
            tesla, text='Load Exact Tesla Defaults',
            command=self.load_tesla_defaults
        ).grid(row=11, column=0, columnspan=2, sticky='ew', pady=(6, 0))

        array_box = ttk.LabelFrame(
            controls, text='Array V5 - Top Coils / Bottom Routing', padding=8
        )
        array_box.pack(fill='x', pady=(0, 8))
        self._entry(array_box, 'Columns', self.array_cols, 0)
        self._entry(array_box, 'Rows (even)', self.array_rows, 1)
        self._entry(array_box, 'Bottom / bridge copper width', self.array_route_width, 2)
        self._entry(array_box, 'Top bridge mask opening', self.array_top_mask_width, 3)
        self._entry(array_box, 'Corner pad offset (array only)', self.array_corner_pad_offset, 4)
        self._entry(array_box, 'ENTRY / EXIT copper rim', self.array_terminal_rim, 5)
        ttk.Label(
            array_box,
            text='ENTRY/EXIT pad Ø = drill Ø + 2 × copper rim.\n'
                 'Default 1.25 mm rim + 1.00 mm drill = 3.50 mm terminal pad.\n'
                 'Corner pad offset is pad-edge distance from the local cell corner.\n'
                 '0.00 mm = pad tangent to the cell corner; larger values move it inward.\n'
                 'The master PCB edge clearance is still added outside the full array.\n'
                 'Pitch auto-sizes from the actual octagon copper envelope.\n'
                 'Safety = half copper width + one wire gap per side.\n'
                 'The 1.25 mm clearance is applied around the full PCB.\n'
                 'Default 2.60 mm mask opening on 3.00 mm bridge leaves\n'
                 '0.20 mm mask overlap per side near the coil.',
            foreground='#555',
            wraplength=300
        ).grid(row=6, column=0, columnspan=2, sticky='w', pady=(5, 5))
        ttk.Button(
            array_box,
            text='Preview Array…',
            command=self.preview_array
        ).grid(row=5, column=0, columnspan=2, sticky='ew', pady=(0, 4))
        ttk.Button(
            array_box,
            text='Export Fusion Array V7 Script…',
            command=self.export_fusion_array_script
        ).grid(row=6, column=0, columnspan=2, sticky='ew')

        lst = ttk.LabelFrame(controls, text='Coils in Area', padding=8)
        lst.pack(fill='both', expand=True, pady=(0, 8))
        self.listbox = tk.Listbox(lst, height=5, exportselection=False)
        self.listbox.pack(fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        lb_buttons = ttk.Frame(lst)
        lb_buttons.pack(fill='x', pady=(6, 0))
        ttk.Button(lb_buttons, text='Delete', command=self.delete_selected).pack(
            side='left', fill='x', expand=True, padx=(0, 3)
        )
        ttk.Button(lb_buttons, text='Reverse', command=self.reverse_selected).pack(
            side='left', fill='x', expand=True, padx=(3, 0)
        )

        self.status = tk.StringVar(value='Ready')
        ttk.Label(controls, textvariable=self.status, wraplength=310).pack(
            fill='x', pady=(8, 0)
        )

        self.canvas = tk.Canvas(
            preview_frame, bg='white', highlightthickness=1,
            highlightbackground='#888'
        )
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.bind('<Configure>', lambda e: self.redraw())

        self.on_geometry_changed()

    def _entry(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=2)
        ttk.Entry(parent, textvariable=var, width=13).grid(
            row=row, column=1, sticky='ew', pady=2
        )
        parent.columnconfigure(1, weight=1)


    def load_tesla_defaults(self):
        # Width/Height are calculated automatically from the coil envelope.

        self.coils = [
            Coil(
                'Coil 1',
                inner_d=13.0, pitch=0.7, turns=8.3,
                copper=0.175, gap=0.175,
                direction='CCW', geometry='Polygon',
                polygon_sides=8, trim_start=5
            ),
            Coil(
                'Coil 2',
                inner_d=13.7, pitch=0.7, turns=7.8,
                copper=0.175, gap=0.175,
                direction='CCW', geometry='Polygon',
                polygon_sides=8, trim_start=1
            )
        ]

        self.show_tesla.set(True)
        self.nail_d.set('5.0')
        self.nail_clearance.set('1.25')
        self.inner_pad_d.set('3.0')
        self.outer_pad_d.set('3.0')
        self.edge_clearance.set('1.25')
        self.pad_angle.set('45.0')
        self.bridge_pad_d.set('3.0')
        self.pad_drill_d.set('1.0')
        self.bridge_drill_d.set('1.0')
        self.duplicate_bottom.set(False)

        self.refresh_list(select=0)
        self.selected = 0
        self.on_select()
        self.redraw()

    def on_geometry_changed(self, event=None):
        if self.geometry.get() == 'Polygon':
            self.sides_entry.configure(state='normal')
        else:
            self.sides_entry.configure(state='disabled')
        self.redraw()

    def get_area(self):
        w, h = float(self.area_w.get()), float(self.area_h.get())
        if w <= 0 or h <= 0:
            raise ValueError('Area width and height must be > 0.')
        return w, h

    def get_form(self):
        vals = [
            float(self.inner_d.get()),
            float(self.pitch.get()),
            float(self.turns.get()),
            float(self.copper.get()),
            float(self.gap.get())
        ]
        if any(v <= 0 for v in vals):
            raise ValueError('All coil dimensions and turns must be > 0.')

        inner, pitch, turns, copper, gap = vals
        geometry = self.geometry.get()

        try:
            polygon_sides = int(self.polygon_sides.get())
            trim_start = int(self.trim_start.get())
        except ValueError:
            raise ValueError('Polygon sides and trim count must be whole numbers.')

        if geometry == 'Polygon' and not (3 <= polygon_sides <= 64):
            raise ValueError('Polygon sides must be between 3 and 64.')
        if trim_start < 0:
            raise ValueError('Trim start vertices cannot be negative.')

        if abs(pitch - (copper + gap)) > 1e-6:
            self.status.set(
                f'Note: pitch {pitch:g} mm differs from '
                f'copper + gap = {copper + gap:g} mm.'
            )

        return (
            inner, pitch, turns, copper, gap,
            self.direction.get(), geometry, polygon_sides, trim_start
        )

    def default_position(self, index, w, h):
        return (w / 2.0, h / 2.0)

    def recenter_coils(self, w, h):
        cx, cy = w / 2.0, h / 2.0
        for c in self.coils:
            c.x = cx
            c.y = cy

    def add_coil(self):
        try:
            w, h = self.get_area()
            data = self.get_form()
            x, y = self.default_position(len(self.coils), w, h)
            c = Coil(f'Coil {len(self.coils) + 1}', *data, x=x, y=y)
            self.coils.append(c)
            self.refresh_list(select=len(self.coils) - 1)
            self.redraw()
        except ValueError as e:
            messagebox.showerror('Invalid value', str(e))

    def update_selected(self):
        if self.selected is None:
            return messagebox.showinfo('Select a coil', 'Select a coil first.')
        try:
            data = self.get_form()
            c = self.coils[self.selected]
            (
                c.inner_d, c.pitch, c.turns, c.copper, c.gap,
                c.direction, c.geometry, c.polygon_sides, c.trim_start
            ) = data
            self.refresh_list(select=self.selected)
            self.redraw()
        except ValueError as e:
            messagebox.showerror('Invalid value', str(e))

    def delete_selected(self):
        if self.selected is None:
            return
        self.coils.pop(self.selected)
        for i, c in enumerate(self.coils):
            c.name = f'Coil {i + 1}'
        self.selected = None
        self.refresh_list()
        self.redraw()

    def reverse_selected(self):
        if self.selected is None:
            return
        c = self.coils[self.selected]
        c.direction = 'CW' if c.direction == 'CCW' else 'CCW'
        self.direction.set(c.direction)
        self.refresh_list(select=self.selected)
        self.redraw()

    def refresh_list(self, select=None):
        self.listbox.delete(0, 'end')
        for c in self.coils:
            shape = (
                f'Poly {c.polygon_sides}'
                if c.geometry == 'Polygon' else 'Circular'
            )
            self.listbox.insert(
                'end',
                f'{c.name}: ID {c.inner_d:g}, P {c.pitch:g}, T {c.turns:g}, '
                f'Cu {c.copper:g}, Gap {c.gap:g}, Trim {c.trim_start}, '
                f'{shape}, {c.direction}'
            )
        if select is not None and self.coils:
            self.listbox.selection_clear(0, 'end')
            self.listbox.selection_set(select)
            self.listbox.activate(select)
            self.selected = select

    def on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected = sel[0]
        c = self.coils[self.selected]
        self.inner_d.set(f'{c.inner_d:g}')
        self.pitch.set(f'{c.pitch:g}')
        self.turns.set(f'{c.turns:g}')
        self.copper.set(f'{c.copper:g}')
        self.gap.set(f'{c.gap:g}')
        self.direction.set(c.direction)
        self.geometry.set(c.geometry)
        self.polygon_sides.set(str(c.polygon_sides))
        self.trim_start.set(str(c.trim_start))
        self.on_geometry_changed()
        self.redraw()

    def circular_spiral_points(self, c, samples_per_turn=90):
        # Archimedean spiral. Inner diameter is the first centerline diameter.
        n = max(20, int(math.ceil(c.turns * samples_per_turn)))
        sign = 1 if c.direction == 'CCW' else -1
        pts = []
        for i in range(n + 1):
            t = 2 * math.pi * c.turns * i / n
            r = c.inner_r + c.pitch * t / (2 * math.pi)
            a = sign * t
            pts.append((c.x + r * math.cos(a), c.y + r * math.sin(a)))
        return pts

    def polygon_spiral_points(self, c):
        """
        Continuous polygon spiral.

        There is one vertex for every polygon side step. For an 8-sided coil,
        that means only 8 segments per turn instead of hundreds of short lines.

        The entered inner diameter is treated as the nominal INSCRIBED
        centerline diameter (apothem diameter). Vertex radius is therefore
        apothem / cos(pi/n).
        """
        sides = max(3, int(c.polygon_sides))
        total_steps = max(1, int(math.ceil(c.turns * sides)))
        sign = 1 if c.direction == 'CCW' else -1
        factor = 1.0 / math.cos(math.pi / sides)

        # Rotate the polygon family by half of one side-step.
        # For an octagon this is 22.5 degrees, which makes the top/bottom
        # sides horizontal and the left/right sides vertical relative to
        # the square PCB.  Pad locations are NOT rotated.
        polygon_rotation = math.pi / sides
        pts = []

        for i in range(total_steps + 1):
            # Clamp the final point exactly to requested turns, including
            # fractional turns.
            turn_fraction = min(i / sides, c.turns)
            t = 2 * math.pi * turn_fraction
            apothem = c.inner_r + c.pitch * turn_fraction
            vertex_r = apothem * factor
            a = polygon_rotation + sign * t
            pts.append((
                c.x + vertex_r * math.cos(a),
                c.y + vertex_r * math.sin(a)
            ))

        # If turns is fractional and did not land on a whole side step,
        # replace/add the exact angular endpoint.
        exact_steps = c.turns * sides
        if abs(exact_steps - round(exact_steps)) > 1e-9:
            t = 2 * math.pi * c.turns
            apothem = c.inner_r + c.pitch * c.turns
            vertex_r = apothem * factor
            a = polygon_rotation + sign * t
            exact_pt = (
                c.x + vertex_r * math.cos(a),
                c.y + vertex_r * math.sin(a)
            )
            # Last generated point may already be clamped to the same exact
            # turn position; overwrite to avoid duplicate segments.
            pts[-1] = exact_pt

        if c.trim_start > 0:
            pts = pts[min(c.trim_start, max(0, len(pts)-2)):]
        return pts

    def spiral_points(self, c, samples_per_turn=90):
        if c.geometry == 'Polygon':
            return self.polygon_spiral_points(c)
        return self.circular_spiral_points(c, samples_per_turn)


    @staticmethod
    def _polyline_length(pts):
        return sum(
            math.hypot(b[0]-a[0], b[1]-a[1])
            for a, b in zip(pts[:-1], pts[1:])
        )


    def array_auto_cell_size(self):
        """Compute square array pitch from the actual two-coil copper envelope."""
        if len(self.coils) < 2:
            raise ValueError('Array auto sizing requires two coils.')

        old_positions = [(c.x, c.y) for c in self.coils]
        try:
            for c in self.coils[:2]:
                c.x = 0.0
                c.y = 0.0

            pts = self.spiral_points(self.coils[0]) + self.spiral_points(self.coils[1])
            min_x = min(p[0] for p in pts)
            max_x = max(p[0] for p in pts)
            min_y = min(p[1] for p in pts)
            max_y = max(p[1] for p in pts)

            span_x = max_x - min_x
            span_y = max_y - min_y
            span = max(span_x, span_y)

            max_copper = max(self.coils[0].copper, self.coils[1].copper)
            max_gap = max(self.coils[0].gap, self.coils[1].gap)

            # Each side gets half the copper width plus one full wire gap.
            side_allowance = max_copper / 2.0 + max_gap
            pitch = span + 2.0 * side_allowance

            return pitch, {
                'span_x': span_x,
                'span_y': span_y,
                'max_copper': max_copper,
                'max_gap': max_gap,
                'side_allowance': side_allowance,
            }
        finally:
            for c, (x, y) in zip(self.coils, old_positions):
                c.x = x
                c.y = y


    def terminal_geometry(self, tg):
        """Return ENTRY/EXIT terminal pad and mask diameters.

        Copper rim is radial annular copper around the plated drill:
            terminal_pad_d = drill_d + 2 * rim

        The terminal solder-mask opening preserves the same radial mask overlap
        used by the normal 3 mm bridge opening. Example:
            bridge pad 3.00, mask 2.60 -> 0.20 mm mask overlap per side.
            terminal pad 3.50 -> terminal mask 3.10 mm.
        """
        rim = float(self.array_terminal_rim.get())
        if rim <= 0:
            raise ValueError('ENTRY / EXIT copper rim must be > 0.')

        drill_d = float(tg['bridge_drill_d'])
        terminal_pad_d = drill_d + 2.0 * rim

        normal_pad_d = float(tg['bridge_pad_d'])
        normal_mask_d = float(self.array_top_mask_width.get())
        radial_mask_overlap = max(0.0, (normal_pad_d - normal_mask_d) / 2.0)
        terminal_mask_d = terminal_pad_d - 2.0 * radial_mask_overlap

        if terminal_mask_d <= drill_d:
            raise ValueError(
                'ENTRY / EXIT mask opening is too small for the terminal drill. '
                'Increase Top bridge mask opening or terminal rim.'
            )

        return {
            'rim': rim,
            'drill_d': drill_d,
            'pad_d': terminal_pad_d,
            'mask_d': terminal_mask_d,
            'mask_overlap': radial_mask_overlap,
        }


    def single_auto_board_size(self):
        """
        Full standalone PCB size.

        Inner cell size is driven by the actual octagon copper envelope:
            outermost centerline + half copper width + one wire gap / side.

        Then the configured PCB clearance is added around the complete cell,
        exactly as it is around the complete array.
        """
        cell_pitch, info = self.array_auto_cell_size()
        edge = float(self.edge_clearance.get())
        board_size = cell_pitch + 2.0 * edge
        return board_size, cell_pitch, info

    def tesla_geometry(self, w, h, corner_pad_offset=None):
        if len(self.coils) < 2:
            return None

        cx, cy = w/2.0, h/2.0
        nail_d = float(self.nail_d.get())
        inner_pad_d = float(self.inner_pad_d.get())
        outer_pad_d = float(self.outer_pad_d.get())
        edge_clear = float(self.edge_clearance.get())

        # Use the same master clearance for the center hole as for the PCB edge.
        # Add one trace gap for manufacturing/DRC safety.
        safety_gap = max(c.gap for c in self.coils[:2]) if self.coils else 0.0
        nail_gap = edge_clear + safety_gap
        self.nail_clearance.set(f'{edge_clear:g}')
        angle = math.radians(float(self.pad_angle.get()))

        # Inner pads tangent to the nail clearance circle.
        pad_center_r = nail_d/2.0 + nail_gap + inner_pad_d/2.0
        c2_inner = (
            cx + pad_center_r * math.cos(angle),
            cy + pad_center_r * math.sin(angle)
        )
        c1_inner = (
            cx - pad_center_r * math.cos(angle),
            cy - pad_center_r * math.sin(angle)
        )

        # Outer pads in opposite corners.
        #
        # Standalone board:
        #   pad edge uses the master PCB edge clearance.
        #
        # Array:
        #   corner_pad_offset is measured from the LOCAL CELL corner to the
        #   PAD EDGE. The complete array already has the master PCB clearance
        #   outside the cell grid, so this lets the connector pads move farther
        #   into the unused inter-cell corner pocket without reducing the
        #   real board-edge clearance.
        if corner_pad_offset is None:
            pad_edge_offset = edge_clear
        else:
            pad_edge_offset = float(corner_pad_offset)
            if pad_edge_offset < 0:
                raise ValueError('Array corner pad offset must be >= 0.')

        inset = pad_edge_offset + outer_pad_d/2.0
        c1_outer = (inset, h-inset)  # NW
        c2_outer = (w-inset, inset)  # SE

        # Additional isolated bridge pad in the NE corner.
        # It has no automatic trace connection; it is intended for a manual
        # jumper / through-layer connection / vertical board stack.
        bridge_pad_d = float(self.bridge_pad_d.get())
        pad_drill_d = float(self.pad_drill_d.get())
        bridge_drill_d = float(self.bridge_drill_d.get())

        if pad_drill_d <= 0 or bridge_drill_d <= 0:
            raise ValueError('Pad drill diameters must be > 0.')
        if pad_drill_d >= min(inner_pad_d, outer_pad_d):
            raise ValueError('Endpoint pad drill must be smaller than the pad diameter.')
        if bridge_drill_d >= bridge_pad_d:
            raise ValueError('Bridge drill must be smaller than the bridge pad diameter.')

        bridge_inset = pad_edge_offset + bridge_pad_d / 2.0
        bridge_pad = (w - bridge_inset, h - bridge_inset)  # NE

        p1 = self.spiral_points(self.coils[0])
        p2 = self.spiral_points(self.coils[1])

        leads = {
            'c1_inner': [p1[0], c1_inner],
            'c2_inner': [p2[0], c2_inner],
            'c1_outer': [p1[-1], c1_outer],
            'c2_outer': [p2[-1], c2_outer],
        }

        return {
            'center': (cx, cy),
            'nail_d': nail_d,
            'nail_clear_d': nail_d + 2.0*nail_gap,
            'nail_effective_clearance': nail_gap,
            'inner_pad_d': inner_pad_d,
            'outer_pad_d': outer_pad_d,
            'c1_inner': c1_inner,
            'c2_inner': c2_inner,
            'c1_outer': c1_outer,
            'c2_outer': c2_outer,
            'bridge_pad': bridge_pad,
            'bridge_pad_d': bridge_pad_d,
            'pad_drill_d': pad_drill_d,
            'bridge_drill_d': bridge_drill_d,
            'leads': leads,
            'p1': p1,
            'p2': p2,
        }

    def redraw(self):
        self.canvas.delete('all')

        # Final V5: standalone Width/Height show the actual PCB size:
        # auto-sized coil envelope + configured exterior clearance.
        if len(self.coils) >= 2:
            try:
                board_size, _, _ = self.single_auto_board_size()
                self.area_w.set(f'{board_size:.6f}')
                self.area_h.set(f'{board_size:.6f}')
            except Exception:
                pass
        try:
            w, h = self.get_area()
        except Exception:
            return

        self.recenter_coils(w, h)
        cw = max(100, self.canvas.winfo_width())
        ch = max(100, self.canvas.winfo_height())
        margin = 35
        scale = min((cw - 2 * margin) / w, (ch - 2 * margin) / h)
        ox = (cw - w * scale) / 2
        oy = (ch - h * scale) / 2

        def cv(p):
            return (ox + p[0] * scale, oy + (h - p[1]) * scale)

        x0, y0 = cv((0, h))
        x1, y1 = cv((w, 0))
        self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', width=2)
        self.canvas.create_text((x0 + x1) / 2, y0 - 15, text=f'{w:g} mm')
        self.canvas.create_text(x0 - 20, (y0 + y1) / 2, text=f'{h:g} mm', angle=90)

        colors = ['#b23a48', '#1261a0', '#25855a', '#8a5a00', '#6b4ca5', '#007f7f']

        total_segments = 0
        for idx, c in enumerate(self.coils):
            pts = self.spiral_points(c)
            total_segments += max(0, len(pts) - 1)
            flat = []
            for p in pts:
                flat.extend(cv(p))

            width = max(1, c.copper * scale)
            color = colors[idx % len(colors)]
            self.canvas.create_line(*flat, fill=color, width=width, smooth=False)

            cx, cy = cv((c.x, c.y))
            rr = c.inner_r * scale
            self.canvas.create_oval(
                cx - rr, cy - rr, cx + rr, cy + rr,
                outline=color, dash=(3, 2)
            )
            self.canvas.create_text(
                cx, cy, text=str(idx + 1), fill=color,
                font=('TkDefaultFont', 9, 'bold')
            )

            if idx == self.selected:
                R = (c.max_centerline_radius + c.copper / 2) * scale
                self.canvas.create_oval(
                    cx - R, cy - R, cx + R, cy + R,
                    outline='#777777', dash=(5, 3), width=2
                )

        extra_status = ''
        if self.show_tesla.get() and len(self.coils) >= 2:
            try:
                tg = self.tesla_geometry(w, h)

                # Nail + clearance reference
                cxp, cyp = cv(tg['center'])
                for diam, color in (
                    (tg['nail_d'], '#00a5b5'),
                    (tg['nail_clear_d'], '#888888'),
                ):
                    rr = diam * scale / 2.0
                    self.canvas.create_oval(
                        cxp-rr, cyp-rr, cxp+rr, cyp+rr,
                        outline=color, width=1
                    )

                # Leads
                lead_colors = {
                    'c1_inner': '#b23a48',
                    'c1_outer': '#b23a48',
                    'c2_inner': '#1261a0',
                    'c2_outer': '#1261a0',
                }
                for name, pts in tg['leads'].items():
                    a = cv(pts[0]); b = cv(pts[1])
                    self.canvas.create_line(
                        a[0], a[1], b[0], b[1],
                        fill=lead_colors[name],
                        width=max(1, 0.175*scale)
                    )

                # Pads
                pads = (
                    (tg['c1_inner'], tg['inner_pad_d'], '#b23a48'),
                    (tg['c2_inner'], tg['inner_pad_d'], '#1261a0'),
                    (tg['c1_outer'], tg['outer_pad_d'], '#b23a48'),
                    (tg['c2_outer'], tg['outer_pad_d'], '#1261a0'),
                )
                for pos, diam, color in pads:
                    x, y = cv(pos)
                    rr = diam * scale / 2.0
                    self.canvas.create_oval(
                        x-rr, y-rr, x+rr, y+rr,
                        outline='#444', fill=color, width=1
                    )

                # Drill holes for the four endpoint pads.
                for pos in (
                    tg['c1_inner'], tg['c2_inner'],
                    tg['c1_outer'], tg['c2_outer']
                ):
                    x, y = cv(pos)
                    rr = tg['pad_drill_d'] * scale / 2.0
                    self.canvas.create_oval(
                        x-rr, y-rr, x+rr, y+rr,
                        outline='#222', fill='white', width=1
                    )

                # Independent NE bridge pad with its own plated-through drill.
                x, y = cv(tg['bridge_pad'])
                rr = tg['bridge_pad_d'] * scale / 2.0
                self.canvas.create_oval(
                    x-rr, y-rr, x+rr, y+rr,
                    outline='#444', fill='#2ca02c', width=1
                )
                rr_hole = tg['bridge_drill_d'] * scale / 2.0
                self.canvas.create_oval(
                    x-rr_hole, y-rr_hole, x+rr_hole, y+rr_hole,
                    outline='#222', fill='white', width=1
                )
                self.canvas.create_text(
                    x, y-rr_hole-7, text='NE Out', fill='#166b16',
                    font=('TkDefaultFont', 8, 'bold')
                )

                # Functional pad names for the standalone preview.
                for pos, name, color, dy in (
                    (tg['c1_outer'], 'C1 Out', '#8b1f2c', -12),
                    (tg['c1_inner'], 'C1 In', '#8b1f2c', 12),
                    (tg['c2_outer'], 'C2 Out', '#0d4778', 12),
                    (tg['c2_inner'], 'C2 In', '#0d4778', -12),
                ):
                    px, py = cv(pos)
                    self.canvas.create_text(
                        px, py + dy, text=name, fill=color,
                        font=('TkDefaultFont', 8, 'bold')
                    )

                l1 = self._polyline_length(tg['p1']) \
                     + self._polyline_length(tg['leads']['c1_inner']) \
                     + self._polyline_length(tg['leads']['c1_outer'])
                l2 = self._polyline_length(tg['p2']) \
                     + self._polyline_length(tg['leads']['c2_inner']) \
                     + self._polyline_length(tg['leads']['c2_outer'])
                extra_status = f' | C1 {l1:.2f} mm | C2 {l2:.2f} mm | Δ {l1-l2:+.2f} mm'
            except Exception as e:
                extra_status = f' | Tesla pad error: {e}'

        self.status.set(
            f'{len(self.coils)} coil(s) | {total_segments} spiral segments | '
            f'Area {w:g} × {h:g} mm{extra_status}'
        )

    def export_dxf(self):
        if not self.coils:
            return messagebox.showinfo('No coils', 'Add at least one coil first.')

        path = filedialog.asksaveasfilename(
            defaultextension='.dxf',
            filetypes=[('DXF files', '*.dxf')]
        )
        if not path:
            return

        try:
            w, h = self.get_area()
            self.recenter_coils(w, h)

            with open(path, 'w', encoding='ascii', errors='ignore') as f:
                def pair(code, val):
                    f.write(f'{code}\n{val}\n')

                pair(0, 'SECTION')
                pair(2, 'HEADER')
                pair(0, 'ENDSEC')
                pair(0, 'SECTION')
                pair(2, 'TABLES')
                pair(0, 'ENDSEC')
                pair(0, 'SECTION')
                pair(2, 'ENTITIES')

                # PCB area outline
                self.write_polyline(
                    f,
                    [(0, 0), (w, 0), (w, h), (0, h), (0, 0)],
                    'AREA'
                )

                for i, c in enumerate(self.coils, 1):
                    # Circular coils use a moderately fine sampling only in
                    # the exported DXF. Polygon coils remain extremely light.
                    pts = self.spiral_points(c, samples_per_turn=120)
                    self.write_polyline(f, pts, f'COIL_{i}')

                    # Inner-diameter reference circle for core/nail clearance.
                    pair(0, 'CIRCLE')
                    pair(8, f'COIL_{i}_REF')
                    pair(10, f'{c.x:.6f}')
                    pair(20, f'{c.y:.6f}')
                    pair(30, '0.0')
                    pair(40, f'{c.inner_r:.6f}')

                if self.show_tesla.get() and len(self.coils) >= 2:
                    tg = self.tesla_geometry(w, h)

                    def circle(center, radius, layer):
                        pair(0, 'CIRCLE')
                        pair(8, layer)
                        pair(10, f'{center[0]:.6f}')
                        pair(20, f'{center[1]:.6f}')
                        pair(30, '0.0')
                        pair(40, f'{radius:.6f}')

                    circle(tg['center'], tg['nail_d']/2.0, 'NAIL_HOLE')
                    circle(tg['center'], tg['nail_clear_d']/2.0, 'NAIL_CLEARANCE')

                    circle(tg['c1_inner'], tg['inner_pad_d']/2.0, 'C1_IN')
                    circle(tg['c2_inner'], tg['inner_pad_d']/2.0, 'C2_IN')
                    circle(tg['c1_outer'], tg['outer_pad_d']/2.0, 'C1_OUT')
                    circle(tg['c2_outer'], tg['outer_pad_d']/2.0, 'C2_OUT')
                    circle(tg['bridge_pad'], tg['bridge_pad_d']/2.0, 'NE_OUT')

                    # Drill references are separate circles/layers in DXF.
                    for pos, layer in (
                        (tg['c1_inner'], 'C1_IN_DRILL'),
                        (tg['c2_inner'], 'C2_IN_DRILL'),
                        (tg['c1_outer'], 'C1_OUT_DRILL'),
                        (tg['c2_outer'], 'C2_OUT_DRILL'),
                    ):
                        circle(pos, tg['pad_drill_d']/2.0, layer)
                    circle(
                        tg['bridge_pad'],
                        tg['bridge_drill_d']/2.0,
                        'NE_OUT_DRILL'
                    )

                    self.write_polyline(f, tg['leads']['c1_inner'], 'C1_IN_LEAD')
                    self.write_polyline(f, tg['leads']['c2_inner'], 'C2_IN_LEAD')
                    self.write_polyline(f, tg['leads']['c1_outer'], 'C1_OUT_LEAD')
                    self.write_polyline(f, tg['leads']['c2_outer'], 'C2_OUT_LEAD')

                pair(0, 'ENDSEC')
                pair(0, 'EOF')

            messagebox.showinfo(
                'DXF exported',
                f'Saved:\n{path}\n\n'
                'Polygon coils export as one lightweight polyline with only '
                'one segment per polygon side.'
            )
        except Exception as e:
            messagebox.showerror('Export failed', str(e))


    @staticmethod
    def _rotate_cw_90_local(p, w, h):
        """Rotate a point 90 degrees clockwise about the cell center."""
        cx, cy = w / 2.0, h / 2.0
        x, y = p
        return (
            cx + (y - cy),
            cy - (x - cx)
        )

    @staticmethod
    def _mirror_ew_local(p, h):
        """Mirror across the east-west midpoint line (horizontal centerline)."""
        x, y = p
        return (x, h - y)

    def _array_local_transform(self, p, w, h, col, row_from_top):
        """
        Reproduce the user's CAD construction exactly.

        Row 1:
          - A1 / column 1: rotate whole cell 90° CW, then mirror across E/W midpoint.
          - columns 2..N: unchanged.

        Row 2:
          - mirror all of Row 1 across the south board edge.
            In local cell coordinates this is y -> h-y.

        Rows 3..N:
          - repeat the Row1/Row2 pair.
        """
        q = p

        # Special A1 cell in the first column of every Row1-type row.
        if col == 0:
            q = self._rotate_cw_90_local(q, w, h)
            q = self._mirror_ew_local(q, h)

        # Every second row is the south-edge mirror of the Row1-type row.
        if row_from_top % 2 == 1:
            q = self._mirror_ew_local(q, h)

        return q

    def _array_global_point(self, p, w, h, col, row_from_top, rows):
        """Transform a cell-local point and translate it into the large PCB."""
        x, y = self._array_local_transform(p, w, h, col, row_from_top)
        # Fusion coordinates use lower-left origin. row_from_top=0 is the top row.
        ox = col * w
        oy = (rows - 1 - row_from_top) * h
        return (x + ox, y + oy)


    def preview_array(self):
        """Interactive CAD-like preview of the complete array."""
        if len(self.coils) < 2:
            return messagebox.showinfo(
                'Need two coils',
                'Array preview expects the two-coil Tesla cell.'
            )

        try:
            cell_pitch, _ = self.array_auto_cell_size()
            w = h = cell_pitch
            cols = int(self.array_cols.get())
            rows = int(self.array_rows.get())
            route_w = float(self.array_route_width.get())
            mask_w = float(self.array_top_mask_width.get())
            board_clear = float(self.edge_clearance.get())

            if cols < 2:
                raise ValueError('Array columns must be at least 2.')
            if rows < 2 or rows % 2:
                raise ValueError('Array rows must be an even number.')
            if route_w <= 0:
                raise ValueError('Routing width must be greater than zero.')
            if mask_w <= 0 or mask_w > route_w:
                raise ValueError(
                    'Top bridge mask opening must be > 0 and no wider than '
                    'the bridge copper width.'
                )

            self.recenter_coils(w, h)
            corner_pad_offset = float(self.array_corner_pad_offset.get())
            if corner_pad_offset < 0:
                raise ValueError('Array corner pad offset must be >= 0.')
            tg = self.tesla_geometry(w, h, corner_pad_offset=corner_pad_offset)
            term = self.terminal_geometry(tg)
            c1, c2 = self.coils[0], self.coils[1]

            board_w = cols * w + 2.0 * board_clear
            board_h = rows * h + 2.0 * board_clear

            def gp(local_pt, col, row):
                p = self._array_global_point(local_pt, w, h, col, row, rows)
                return (p[0] + board_clear, p[1] + board_clear)

            def gpoly(local_pts, col, row):
                return [gp(p, col, row) for p in local_pts]

            win = tk.Toplevel(self)
            win.title(
                f'Array Preview — {cols} × {rows} cells — '
                f'{board_w:.2f} × {board_h:.2f} mm'
            )
            win.geometry('1400x900')
            win.minsize(850, 550)

            main = ttk.Frame(win)
            main.pack(fill='both', expand=True)
            main.columnconfigure(0, weight=1)
            main.rowconfigure(0, weight=1)

            cv = tk.Canvas(
                main, bg='#1f252b', highlightthickness=0,
                cursor='crosshair'
            )
            cv.grid(row=0, column=0, sticky='nsew')

            side = ttk.Frame(main, padding=8)
            side.grid(row=0, column=1, sticky='ns')

            ttk.Label(side, text='Preview Layers',
                      font=('TkDefaultFont', 10, 'bold')).pack(
                anchor='w', pady=(0, 6)
            )

            layer_vars = {
                'board': tk.BooleanVar(value=True),
                'grid': tk.BooleanVar(value=False),
                'top_coils': tk.BooleanVar(value=True),
                'top_bridges': tk.BooleanVar(value=True),
                'bottom_routing': tk.BooleanVar(value=True),
                'vias': tk.BooleanVar(value=True),
                'holes': tk.BooleanVar(value=True),
                'top_mask': tk.BooleanVar(value=True),
                'names': tk.BooleanVar(value=False),
            }

            labels = [
                ('board', 'Board outline'),
                ('grid', 'Cell grid'),
                ('top_coils', 'Coil 1 / Coil 2'),
                ('top_bridges', 'Top Bridge'),
                ('bottom_routing', 'Bottom Bridge'),
                ('vias', 'Named Pads / PTH vias'),
                ('holes', 'Nail holes'),
                ('top_mask', f'Top mask opening ({mask_w:g} mm)'),
                ('names', 'Object names'),
            ]

            # View transform in pixels/mm. World coordinates are mm with +Y up.
            state = {
                'scale': 1.0,
                'ox': 0.0,
                'oy': 0.0,
                'pan_x': 0,
                'pan_y': 0,
            }

            def world_to_screen(p):
                x, y = p
                return (
                    state['ox'] + x * state['scale'],
                    state['oy'] - y * state['scale']
                )

            def flat(points):
                out = []
                for p in points:
                    sx, sy = world_to_screen(p)
                    out.extend((sx, sy))
                return out

            def px_width(mm, minimum=1):
                return max(minimum, mm * state['scale'])

            def draw_line(points, fill, width_mm, dash=None):
                if len(points) < 2:
                    return
                cv.create_line(
                    *flat(points),
                    fill=fill,
                    width=px_width(width_mm),
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                    dash=dash
                )

            def draw_circle(center, diameter, outline, width=1, fill=''):
                cx, cy = world_to_screen(center)
                r = diameter * state['scale'] / 2.0
                cv.create_oval(
                    cx-r, cy-r, cx+r, cy+r,
                    outline=outline, width=width, fill=fill
                )

            def redraw_preview():
                cv.delete('all')

                # Board
                if layer_vars['board'].get():
                    p0 = world_to_screen((0, 0))
                    p1 = world_to_screen((board_w, board_h))
                    cv.create_rectangle(
                        p0[0], p1[1], p1[0], p0[1],
                        outline='#f5d742', width=2
                    )

                # Construction cell grid.
                if layer_vars['grid'].get():
                    for col in range(cols + 1):
                        x = board_clear + col * w
                        draw_line(
                            [(x, board_clear),
                             (x, board_clear + rows*h)],
                            '#66717a', 0.04
                        )
                    for rr in range(rows + 1):
                        y = board_clear + rr * h
                        draw_line(
                            [(board_clear, y),
                             (board_clear + cols*w, y)],
                            '#66717a', 0.04
                        )

                # Top coils.
                if layer_vars['top_coils'].get():
                    for row in range(rows):
                        for col in range(cols):
                            draw_line(
                                gpoly(tg['p1'], col, row),
                                '#ff3333', c1.copper
                            )
                            draw_line(
                                gpoly(tg['leads']['c1_inner'], col, row),
                                '#ff3333', c1.copper
                            )
                            draw_line(
                                gpoly(tg['leads']['c1_outer'], col, row),
                                '#ff3333', c1.copper
                            )
                            draw_line(
                                gpoly(tg['p2'], col, row),
                                '#2e63ff', c2.copper
                            )
                            draw_line(
                                gpoly(tg['leads']['c2_inner'], col, row),
                                '#2e63ff', c2.copper
                            )
                            draw_line(
                                gpoly(tg['leads']['c2_outer'], col, row),
                                '#2e63ff', c2.copper
                            )

                # Top bridges: horizontal cell-to-cell bridges PLUS all
                # row-to-row turnarounds. These are intentionally exposed
                # copper interfaces for stacking / experimental access.
                if layer_vars['top_bridges'].get():
                    for row in range(rows):
                        for col in range(cols - 1):
                            draw_line(
                                [
                                    gp(tg['bridge_pad'], col, row),
                                    gp(tg['c1_outer'], col + 1, row),
                                ],
                                '#ff9f1c', route_w
                            )

                    # Left turnarounds within each 2-row block.
                    for top_row in range(0, rows, 2):
                        bottom_row = top_row + 1
                        draw_line(
                            [
                                gp(tg['c1_outer'], 0, top_row),
                                gp(tg['c1_outer'], 0, bottom_row),
                            ],
                            '#ff9f1c', route_w
                        )

                    # Right-side joins between row pairs.
                    for upper_row in range(1, rows - 1, 2):
                        lower_row = upper_row + 1
                        draw_line(
                            [
                                gp(tg['bridge_pad'], cols - 1, upper_row),
                                gp(tg['bridge_pad'], cols - 1, lower_row),
                            ],
                            '#ff9f1c', route_w
                        )

                # Bottom routing.
                if layer_vars['bottom_routing'].get():
                    for row in range(rows):
                        for col in range(cols):
                            draw_line(
                                [
                                    gp(tg['c1_inner'], col, row),
                                    gp(tg['c2_outer'], col, row),
                                ],
                                '#20d070', route_w
                            )
                            draw_line(
                                [
                                    gp(tg['c2_inner'], col, row),
                                    gp(tg['bridge_pad'], col, row),
                                ],
                                '#20d070', route_w
                            )

                # Vias
                if layer_vars['vias'].get():
                    for row in range(rows):
                        for col in range(cols):
                            for pad_name, dia in (
                                ('c1_inner', tg['inner_pad_d']),
                                ('c2_inner', tg['inner_pad_d']),
                                ('c1_outer', tg['outer_pad_d']),
                                ('c2_outer', tg['outer_pad_d']),
                                ('bridge_pad', tg['bridge_pad_d']),
                            ):
                                p = gp(tg[pad_name], col, row)
                                # ENTRY and EXIT are intentionally larger,
                                # mechanically robust solder terminals.
                                if (
                                    pad_name == 'bridge_pad'
                                    and col == cols - 1
                                    and row in (0, rows - 1)
                                ):
                                    dia = term['pad_d']
                                draw_circle(
                                    p, dia, '#d8d8d8', 1, '#555b60'
                                )

                # Nail holes
                if layer_vars['holes'].get():
                    for row in range(rows):
                        for col in range(cols):
                            p = gp(tg['center'], col, row)
                            draw_circle(
                                p, tg['nail_d'],
                                '#eeeeee', 1, '#111418'
                            )

                # Top soldermask opening. Draw as cyan outline over the bridge,
                # not as a filled region, so copper underneath remains visible.
                if layer_vars['top_mask'].get():
                    for row in range(rows):
                        for col in range(cols - 1):
                            draw_line(
                                [
                                    gp(tg['bridge_pad'], col, row),
                                    gp(tg['c1_outer'], col + 1, row),
                                ],
                                '#62e6ff', mask_w
                            )
                    # Row-to-row turnaround TOP mask openings.
                    for top_row in range(0, rows, 2):
                        bottom_row = top_row + 1
                        draw_line(
                            [
                                gp(tg['c1_outer'], 0, top_row),
                                gp(tg['c1_outer'], 0, bottom_row),
                            ],
                            '#62e6ff', mask_w
                        )
                    for upper_row in range(1, rows - 1, 2):
                        lower_row = upper_row + 1
                        draw_line(
                            [
                                gp(tg['bridge_pad'], cols - 1, upper_row),
                                gp(tg['bridge_pad'], cols - 1, lower_row),
                            ],
                            '#62e6ff', mask_w
                        )

                    # Entry/exit top openings.
                    entry = gp(tg['bridge_pad'], cols - 1, 0)
                    exitp = gp(tg['bridge_pad'], cols - 1, rows - 1)
                    draw_circle(
                        entry, term['mask_d'],
                        '#62e6ff', 2
                    )
                    draw_circle(
                        exitp, term['mask_d'],
                        '#62e6ff', 2
                    )

                # Functional object names. These are documentation/preview
                # labels only; they do not change the ARRAY electrical net.
                if layer_vars['names'].get():
                    # Label one representative cell to avoid turning the full
                    # 64-cell preview into a wall of text.
                    label_col = min(1, cols - 1)
                    label_row = 0

                    def label_at(local_pt, name, dx=0, dy=0, fill='#ffffff'):
                        sx, sy = world_to_screen(gp(local_pt, label_col, label_row))
                        cv.create_text(
                            sx + dx, sy + dy, text=name, fill=fill,
                            font=('TkDefaultFont', 8, 'bold')
                        )

                    label_at(tg['c1_outer'], 'C1 Out', dy=-12, fill='#ff7777')
                    label_at(tg['c1_inner'], 'C1 In', dy=12, fill='#ff7777')
                    label_at(tg['c2_outer'], 'C2 Out', dy=12, fill='#7794ff')
                    label_at(tg['c2_inner'], 'C2 In', dy=-12, fill='#7794ff')
                    label_at(tg['bridge_pad'], 'NE Out', dy=-12, fill='#8dff9e')

                    # Coil names near their approximate center.
                    cc = gp(tg['center'], label_col, label_row)
                    csx, csy = world_to_screen(cc)
                    cv.create_text(
                        csx, csy - 18, text='Coil 1', fill='#ff7777',
                        font=('TkDefaultFont', 8, 'bold')
                    )
                    cv.create_text(
                        csx, csy + 18, text='Coil 2', fill='#7794ff',
                        font=('TkDefaultFont', 8, 'bold')
                    )

                    # Global terminals are always named explicitly.
                    for p, name in (
                        (gp(tg['bridge_pad'], cols - 1, 0), 'Enter Pad'),
                        (gp(tg['bridge_pad'], cols - 1, rows - 1), 'Exit Pad'),
                    ):
                        sx, sy = world_to_screen(p)
                        cv.create_text(
                            sx + 8, sy - 12, text=name, anchor='w',
                            fill='#fff3a6',
                            font=('TkDefaultFont', 9, 'bold')
                        )

                # Small status text in upper-left.
                cv.create_text(
                    12, 12, anchor='nw', fill='#d6dde3',
                    text=(
                        f'Board {board_w:.2f} × {board_h:.2f} mm   '
                        f'Cell pitch {w:.3f} mm   '
                        f'Copper {route_w:.2f} mm   '
                        f'Mask {mask_w:.2f} mm   '
                        f'Terminal Ø {term["pad_d"]:.2f} mm'
                    )
                )

            def fit_view(event=None):
                cw = max(cv.winfo_width(), 100)
                ch = max(cv.winfo_height(), 100)
                margin = 40
                sx = (cw - 2*margin) / board_w
                sy = (ch - 2*margin) / board_h
                state['scale'] = max(0.05, min(sx, sy))
                state['ox'] = (cw - board_w * state['scale']) / 2.0
                state['oy'] = (ch + board_h * state['scale']) / 2.0
                redraw_preview()

            def zoom_at(x, y, factor):
                old = state['scale']
                new = max(0.05, min(old * factor, 500.0))
                if abs(new - old) < 1e-12:
                    return

                # World point under cursor before zoom.
                wx = (x - state['ox']) / old
                wy = (state['oy'] - y) / old

                state['scale'] = new
                state['ox'] = x - wx * new
                state['oy'] = y + wy * new
                redraw_preview()

            def on_wheel(event):
                factor = 1.18 if event.delta > 0 else 1/1.18
                zoom_at(event.x, event.y, factor)
                return 'break'

            def on_linux_up(event):
                zoom_at(event.x, event.y, 1.18)
                return 'break'

            def on_linux_down(event):
                zoom_at(event.x, event.y, 1/1.18)
                return 'break'

            def pan_start(event):
                state['pan_x'] = event.x
                state['pan_y'] = event.y
                cv.configure(cursor='fleur')
                return 'break'

            def pan_move(event):
                dx = event.x - state['pan_x']
                dy = event.y - state['pan_y']
                state['pan_x'] = event.x
                state['pan_y'] = event.y
                state['ox'] += dx
                state['oy'] += dy
                redraw_preview()
                return 'break'

            def pan_end(event):
                cv.configure(cursor='crosshair')
                return 'break'

            # Middle mouse = CAD-style pan.
            cv.bind('<ButtonPress-2>', pan_start)
            cv.bind('<B2-Motion>', pan_move)
            cv.bind('<ButtonRelease-2>', pan_end)

            # Mouse wheel = cursor-centered zoom.
            cv.bind('<MouseWheel>', on_wheel)
            cv.bind('<Button-4>', on_linux_up)
            cv.bind('<Button-5>', on_linux_down)

            # Fit shortcuts.
            cv.bind('<Double-Button-2>', fit_view)
            cv.bind('<KeyPress-f>', fit_view)
            cv.bind('<KeyPress-F>', fit_view)
            cv.focus_set()

            for key, label in labels:
                ttk.Checkbutton(
                    side, text=label, variable=layer_vars[key],
                    command=redraw_preview
                ).pack(anchor='w', pady=1)

            ttk.Separator(side, orient='horizontal').pack(
                fill='x', pady=8
            )
            ttk.Button(side, text='Fit Board', command=fit_view).pack(
                fill='x', pady=(0, 4)
            )
            ttk.Button(side, text='Close', command=win.destroy).pack(
                fill='x'
            )

            ttk.Label(
                side,
                text=(
                    '\\nMouse controls:\\n'
                    'Wheel = zoom at cursor\\n'
                    'Middle-button hold = pan\\n'
                    'Double middle = fit\\n'
                    'F = fit board'
                ),
                foreground='#555',
                justify='left'
            ).pack(anchor='w')

            win.after(100, fit_view)

        except Exception as e:
            messagebox.showerror('Array preview failed', str(e))


    def export_fusion_array_script(self):
        """
        Export Array V5 using the routing pattern proven in the user's CAD sketch.

        Electrical path per cell on Bottom:
            C1 inner -> C2 outer
            C2 inner -> bridge

        Between adjacent cells in every row:
            bridge(left cell) -> C1 outer(right cell)

        Row turnarounds:
            Row1->2, Row3->4, ...:
                C1 outer of special A1 cell -> C1 outer of mirrored A1 cell
            Row2->3, Row4->5, Row6->7, ...:
                bridge of right-most cell -> bridge of next row right-most cell

        This creates one continuous boustrophedon series path:
            entry = bridge at upper-right
            exit  = bridge at lower-right

        Top contains coils only. Bottom contains routing only.
        """
        if len(self.coils) < 2:
            return messagebox.showinfo(
                'Need two coils',
                'Array V5 expects the proven two-coil Tesla cell.'
            )

        path = filedialog.asksaveasfilename(
            defaultextension='.scr',
            filetypes=[('Fusion / EAGLE script', '*.scr'), ('All files', '*.*')]
        )
        if not path:
            return

        try:
            cell_pitch, pitch_info = self.array_auto_cell_size()
            w = h = cell_pitch

            cols = int(self.array_cols.get())
            rows = int(self.array_rows.get())
            route_w = float(self.array_route_width.get())
            mask_w = float(self.array_top_mask_width.get())

            if cols < 2:
                raise ValueError('Array columns must be at least 2.')
            if rows < 2 or rows % 2:
                raise ValueError('Array rows must be an even number (2, 4, 6, 8...).')
            if route_w <= 0:
                raise ValueError('Bottom route width must be > 0.')
            if mask_w <= 0 or mask_w > route_w:
                raise ValueError(
                    'Top bridge mask opening must be > 0 and no wider than '
                    'the bridge copper width.'
                )

            self.recenter_coils(w, h)
            corner_pad_offset = float(self.array_corner_pad_offset.get())
            if corner_pad_offset < 0:
                raise ValueError('Array corner pad offset must be >= 0.')
            tg = self.tesla_geometry(w, h, corner_pad_offset=corner_pad_offset)
            term = self.terminal_geometry(tg)
            c1 = self.coils[0]
            c2 = self.coils[1]

            board_clear = float(self.edge_clearance.get())
            board_w = cols * w + 2.0 * board_clear
            board_h = rows * h + 2.0 * board_clear

            def gp(local_pt, col, row):
                p = self._array_global_point(local_pt, w, h, col, row, rows)
                return (p[0] + board_clear, p[1] + board_clear)

            def gpoly(local_pts, col, row):
                return [gp(p, col, row) for p in local_pts]

            def xy(p):
                return f'({p[0]:.6f} {p[1]:.6f})'

            def line_command(signal, width, pts):
                coords = ' '.join(xy(p) for p in pts)
                return f"LINE '{signal}' {width:.6f} {coords};"

            # All copper belongs to one continuous physical conductor.
            signal = 'ARRAY'

            with open(path, 'w', encoding='ascii', errors='ignore') as f:
                f.write("# WYLAS Bifilar Array Final V17 - TOP exposed row turnarounds\n")
                f.write("# Top = bifilar coils + exposed cell/row bridges; Bottom = internal cell routing only\n")
                f.write("# FUNCTIONAL OBJECT NAMES (documentation only; electrical net remains ARRAY)\n")
                f.write("# Coil 1 = first/red bifilar spiral\n")
                f.write("# Coil 2 = second/blue bifilar spiral\n")
                f.write("# Top Bridge = horizontal cell-to-cell bridge on Top\n")
                f.write("# Bottom Bridge = internal cell routing on Bottom\n")
                f.write("# Internal pads = C1 Out, C1 In, C2 Out, C2 In, NE Out\n")
                f.write("# Enter Pad = upper-right array NE Out terminal\n")
                f.write("# Exit Pad = lower-right array NE Out terminal\n")
                f.write(
                    "# A1 special transform = 90 deg CW, then mirror E/W midpoint\n"
                )
                f.write("# Row2 = mirror Row1 across south cell edge; pair repeats\n\n")
                f.write("GRID MM 0.01 ON;\n")
                f.write("SET WIRE_BEND 2;\n")
                f.write(f"# Auto cell pitch: {w:.6f} mm\n")
                f.write(f"# Exterior clearance: {board_clear:.6f} mm\n")
                f.write(f"# Nail effective clearance: {tg['nail_effective_clearance']:.6f} mm\n")
                f.write(f"# Top bridge copper width: {route_w:.6f} mm\n")
                f.write(f"# Top bridge mask opening: {mask_w:.6f} mm\n\n")

                # One physical board outline; internal 26 mm cell boundaries are
                # construction logic only and are intentionally NOT cut lines.
                f.write("LAYER BoardOutline;\n")
                f.write(
                    "LINE 0 "
                    f"(0 0) ({board_w:.6f} 0) "
                    f"({board_w:.6f} {board_h:.6f}) "
                    f"(0 {board_h:.6f}) (0 0);\n\n"
                )

                # ---------- COIL 1 / COIL 2: all requested bifilar cells ----------
                f.write("LAYER Top;\n")
                for row in range(rows):
                    for col in range(cols):
                        f.write(
                            line_command(signal, c1.copper, gpoly(tg['p1'], col, row))
                            + "\n"
                        )
                        f.write(
                            line_command(
                                signal, c1.copper,
                                gpoly(tg['leads']['c1_inner'], col, row)
                            ) + "\n"
                        )
                        f.write(
                            line_command(
                                signal, c1.copper,
                                gpoly(tg['leads']['c1_outer'], col, row)
                            ) + "\n"
                        )
                        f.write(
                            line_command(signal, c2.copper, gpoly(tg['p2'], col, row))
                            + "\n"
                        )
                        f.write(
                            line_command(
                                signal, c2.copper,
                                gpoly(tg['leads']['c2_inner'], col, row)
                            ) + "\n"
                        )
                        f.write(
                            line_command(
                                signal, c2.copper,
                                gpoly(tg['leads']['c2_outer'], col, row)
                            ) + "\n"
                        )
                f.write("\n")


                # ---------- TOP BRIDGE: 3 mm cell-to-cell bridges ----------
                # Preserve the original electrical routing topology, but place
                # every horizontal cell-to-cell bridge on TOP copper so it is
                # physically accessible for soldering.
                #
                # Connection at each horizontal boundary:
                #     bridge pad of left cell -> C1 outer pad of right cell
                #
                # Width matches the 3 mm via/pad diameter.
                f.write("\n# TOP cell-to-cell solder bridges\n")
                f.write("LAYER Top;\n")
                for row in range(rows):
                    for col in range(cols - 1):
                        f.write(
                            line_command(
                                signal, route_w,
                                [
                                    gp(tg['bridge_pad'], col, row),
                                    gp(tg['c1_outer'], col + 1, row),
                                ]
                            ) + "\n"
                        )
                # Row-to-row turnarounds are also TOP copper so every
                # serpentine transition is accessible from the same side.
                for top_row in range(0, rows, 2):
                    bottom_row = top_row + 1
                    f.write(
                        line_command(
                            signal, route_w,
                            [
                                gp(tg['c1_outer'], 0, top_row),
                                gp(tg['c1_outer'], 0, bottom_row),
                            ]
                        ) + "\n"
                    )
                for upper_row in range(1, rows - 1, 2):
                    lower_row = upper_row + 1
                    f.write(
                        line_command(
                            signal, route_w,
                            [
                                gp(tg['bridge_pad'], cols - 1, upper_row),
                                gp(tg['bridge_pad'], cols - 1, lower_row),
                            ]
                        ) + "\n"
                    )
                f.write("\n")

                # ---------- PTH endpoints / bridge pads and NPTH nail holes ----------
                # These are the ONLY two external solder interfaces on the board.
                entry = gp(tg['bridge_pad'], cols - 1, 0)
                exitp = gp(tg['bridge_pad'], cols - 1, rows - 1)

                # Pad naming:
                #   c1_outer  = C1 Out
                #   c1_inner  = C1 In
                #   c2_outer  = C2 Out
                #   c2_inner  = C2 In
                #   bridge_pad = NE Out
                #
                # Fusion-native tented-via fix:
                # Set STOP OFF BEFORE VIA creation so new vias inherit
                # Solder Mask = Off instead of Fusion's newer Auto default.
                f.write("CHANGE STOP OFF;\n")
                f.write(f"CHANGE DRILL {tg['pad_drill_d']:.6f};\n")
                for row in range(rows):
                    for col in range(cols):
                        for pad_name, pad_d in (
                            ('c1_inner', tg['inner_pad_d']),
                            ('c2_inner', tg['inner_pad_d']),
                            ('c1_outer', tg['outer_pad_d']),
                            ('c2_outer', tg['outer_pad_d']),
                        ):
                            f.write(
                                f"VIA '{signal}' {pad_d:.6f} "
                                f"{xy(gp(tg[pad_name], col, row))};\n"
                            )

                # Bridge pads use their own drill setting, but are on ARRAY net.
                f.write(f"CHANGE DRILL {tg['bridge_drill_d']:.6f};\n")
                for row in range(rows):
                    for col in range(cols):
                        pad_d = tg['bridge_pad_d']
                        if col == cols - 1 and row in (0, rows - 1):
                            pad_d = term['pad_d']
                        f.write(
                            f"VIA '{signal}' {pad_d:.6f} "
                            f"{xy(gp(tg['bridge_pad'], col, row))};\n"
                        )
                f.write("\n")

                # ---------- SOLDER MASK / PCBWAY INTERFACE ----------
                # Array mask strategy:
                #
                #   * Every via starts TENTED / covered (STOP OFF).
                #   * Each TOP cell-to-cell bridge gets ONE narrower tStop LINE.
                #     Default 2.60 mm on 3.00 mm copper leaves 0.20 mm
                #     soldermask overlap on each side for coil safety.
                #
                # A thick tStop LINE forms a capsule-shaped opening with rounded
                # ends.  It exposes the 3 mm bridge and its two end-via annuli
                # without using the old oversized square openings that could
                # overlap and expose nearby coil turns.
                #
                #   * ENTRY and EXIT are exposed with small square openings only
                #     because they are standalone interface pads at the board edge.
                #   * No bStop geometry is created, so Bottom remains protected.
                f.write("\n# PCBWay soldermask control - capsule openings\n")

                # Suppress automatic soldermask openings on EVERY via first.
                for row in range(rows):
                    for col in range(cols):
                        for pad_name in (
                            'c1_inner', 'c2_inner', 'c1_outer', 'c2_outer',
                            'bridge_pad'
                        ):
                            f.write(
                                f"CHANGE STOP OFF {xy(gp(tg[pad_name], col, row))};\n"
                            )

                # Open TOP soldermask only along the center of the horizontal
                # copper bridge. The mask opening is intentionally narrower
                # than the copper to leave a protected margin near the coils.
                f.write("LAYER tStop;\n")
                mask_trace_w = mask_w

                for row in range(rows):
                    for col in range(cols - 1):
                        p1 = gp(tg['bridge_pad'], col, row)
                        p2 = gp(tg['c1_outer'], col + 1, row)
                        f.write(
                            f"LINE {mask_trace_w:.6f} {xy(p1)} {xy(p2)};\n"
                        )

                # Expose TOP row-to-row turnarounds with the same
                # inset capsule opening used on horizontal bridges.
                for top_row in range(0, rows, 2):
                    bottom_row = top_row + 1
                    p1 = gp(tg['c1_outer'], 0, top_row)
                    p2 = gp(tg['c1_outer'], 0, bottom_row)
                    f.write(
                        f"LINE {mask_trace_w:.6f} {xy(p1)} {xy(p2)};\n"
                    )
                for upper_row in range(1, rows - 1, 2):
                    lower_row = upper_row + 1
                    p1 = gp(tg['bridge_pad'], cols - 1, upper_row)
                    p2 = gp(tg['bridge_pad'], cols - 1, lower_row)
                    f.write(
                        f"LINE {mask_trace_w:.6f} {xy(p1)} {xy(p2)};\n"
                    )

                # ENTRY / EXIT use near-circular TOP soldermask openings.
                # A very short tStop LINE with round endcaps avoids the square
                # openings from the earlier versions.
                interface_mask_d = term['mask_d']
                interface_half_len = 0.05  # 0.10 mm total; visually/functionally round
                for p in (entry, exitp):
                    p1 = (p[0] - interface_half_len, p[1])
                    p2 = (p[0] + interface_half_len, p[1])
                    f.write(
                        f"LINE {interface_mask_d:.6f} {xy(p1)} {xy(p2)};\n"
                    )

                # No bStop openings are written: Bottom stays soldermask-covered.

                # ---------- MINIMAL SILKSCREEN ID ----------
                # One small board identifier on each side keeps the silkscreen
                # Gerbers non-empty without cluttering the coil array.
                silk_x = 1.50
                silk_y = 0.75
                f.write("LAYER tPlace;\n")
                f.write("CHANGE SIZE 1.000000;\n")
                f.write("CHANGE RATIO 18;\n")
                f.write(f"TEXT 'WYLAR_V1' R0 ({silk_x:.6f} {silk_y:.6f});\n")
                f.write("LAYER bPlace;\n")
                f.write("CHANGE SIZE 1.000000;\n")
                f.write("CHANGE RATIO 18;\n")
                f.write(f"TEXT 'WYLAR_V1' MR0 ({silk_x:.6f} {silk_y:.6f});\n")

                f.write("LAYER Bottom;\n\n")

                # Non-plated nail holes.
                for row in range(rows):
                    for col in range(cols):
                        f.write(
                            f"HOLE {tg['nail_d']:.6f} "
                            f"{xy(gp(tg['center'], col, row))};\n"
                        )
                f.write("\n")

                # ---------- BOTTOM BRIDGE: internal / row routing only ----------
                f.write("LAYER Bottom;\n")

                # 1) Internal cell series links.
                #    These are transformed with the whole cell, including A1.
                for row in range(rows):
                    for col in range(cols):
                        f.write(
                            line_command(
                                signal, route_w,
                                [
                                    gp(tg['c1_inner'], col, row),
                                    gp(tg['c2_outer'], col, row),
                                ]
                            ) + "\n"
                        )
                        f.write(
                            line_command(
                                signal, route_w,
                                [
                                    gp(tg['c2_inner'], col, row),
                                    gp(tg['bridge_pad'], col, row),
                                ]
                            ) + "\n"
                        )

                # 2) Horizontal cell-to-cell bridges are intentionally
                # NOT drawn on Bottom.  They were moved to Top copper above,
                # at the same 3 mm width as the Bottom routing and PTH pads.

                # 3) Row turnarounds are intentionally NOT drawn on Bottom.
                #    They are generated on Top above and exposed through tStop.

                # ENTER PAD / EXIT PAD: the only two external array terminals.
                f.write("\n# EXPOSED PCB INTERFACES ONLY\n")
                f.write("# ENTER PAD (upper-right NE Out): "
                        f"{xy(entry)}\n")
                f.write("# EXIT PAD  (lower-right NE Out): "
                        f"{xy(exitp)}\n")

                f.write(
                    "\nDISPLAY Top Bottom Pads Vias BoardOutline Drills Holes;\n"
                )
                f.write("WINDOW FIT;\n")

                # Experimental Fusion bulk via-mask automation.
                # Restrict selection to VIA objects only, group all of them,
                # then apply STOP OFF to the whole group.
                f.write("\n# --- BULK VIA SOLDER MASK OFF ---\n")
                f.write("SET SELECTION_FILTER ON;\n")
                f.write("SET SELECTTYPES NONE VIA;\n")
                f.write("GROUP ALL;\n")
                f.write("CHANGE STOP OFF (> 0 0);\n")
                f.write("GROUP;\n")
                f.write("SET SELECTTYPES ALL;\n")
                f.write("SET SELECTION_FILTER OFF;\n")
                f.write("# --- END BULK VIA SOLDER MASK OFF ---\n")
            messagebox.showinfo(
                'Fusion Array V5 exported',
                f'Saved:\\n{path}\\n\\n'
                f'Auto cell pitch: {w:.3f} × {h:.3f} mm\\n'
                f'Board: {board_w:.3f} × {board_h:.3f} mm\\n'
                f'Cells: {cols} × {rows} = {cols*rows}\\n'
                f'Exterior clearance: {board_clear:g} mm\\n'
                f'Nail effective clearance: {tg["nail_effective_clearance"]:.3f} mm\\n\\n'
                'Top: coils only\\n'
                'Bottom: 3 mm internal routing + row turnarounds\\n'
                'Top: 3 mm horizontal cell-to-cell bridges\\n'
                'PCBWay mask: horizontal bridges exposed through inset capsule openings on TOP only.\\n'
                'ENTRY/EXIT use rounded TOP-only mask openings.\\n'
                'Bottom side stays soldermask-covered.\\n'
                'All other vias remain covered on both sides.\\n'
                'Special A1 and Row2-3 / Row4-5 / Row6-7 transitions are '
                'generated explicitly.'
            )
        except Exception as e:
            messagebox.showerror('Array export failed', str(e))


    def export_fusion_script(self):
        """
        Export one complete standalone PCB using the SAME architecture as Array V5:

          TOP:
            - bifilar coils
            - only the two board interface vias exposed

          PTH:
            - four coil endpoint vias
            - NE bridge via

          BOTTOM:
            - 3 mm internal series routing
            - C1 inner -> C2 outer
            - C2 inner -> bridge

          BOARD:
            - auto-sized from actual octagon copper extents
            - configured edge clearance added around the full board
            - nail clearance follows the same master clearance

        The two standalone board interfaces are:
            ENTRY = NE bridge via
            EXIT  = C1 outer via

        All other vias are soldermask-covered on both sides.
        ENTRY and EXIT are exposed on TOP only.
        """
        if len(self.coils) < 2:
            return messagebox.showinfo(
                'Need two coils',
                'The single PCB export expects the two-coil Tesla layout.'
            )

        path = filedialog.asksaveasfilename(
            defaultextension='.scr',
            filetypes=[('Fusion / EAGLE script', '*.scr'), ('All files', '*.*')]
        )
        if not path:
            return

        try:
            board_size, cell_pitch, pitch_info = self.single_auto_board_size()
            w = h = board_size
            route_w = float(self.array_route_width.get())
            if route_w <= 0:
                raise ValueError('Bottom route width must be > 0.')

            # For a standalone board, the coils are centered in the full board.
            # tesla_geometry() then places the exterior pads exactly the configured
            # distance from the real board outline.
            self.recenter_coils(w, h)
            tg = self.tesla_geometry(w, h)
            term = self.terminal_geometry(tg)

            c1 = self.coils[0]
            c2 = self.coils[1]

            def xy(p):
                return f'({p[0]:.6f} {p[1]:.6f})'

            def line_command(signal, width, pts):
                coords = ' '.join(xy(p) for p in pts)
                return f"LINE '{signal}' {width:.6f} {coords};"

            # One continuous electrical conductor after Bottom routing is added.
            signal = 'CELL'

            # Standalone external terminals.
            entry = tg['bridge_pad']
            exitp = tg['c1_outer']

            with open(path, 'w', encoding='ascii', errors='ignore') as f:
                f.write("# WYLAS Bifilar Standalone PCB Final V5\n")
                f.write("# Top = Coil 1 / Coil 2; Bottom = Bottom Bridge\n")
                f.write("# FUNCTIONAL OBJECT NAMES (documentation only; electrical net remains CELL)\n")
                f.write("# Internal pads = C1 Out, C1 In, C2 Out, C2 In, NE Out\n")
                f.write("# Enter Pad = NE Out; Exit Pad = C1 Out\n")
                f.write("# Only Enter Pad / Exit Pad exposed on Top soldermask\n\n")

                f.write("GRID MM 0.01 ON;\n")
                f.write("SET WIRE_BEND 2;\n")
                f.write(f"# Auto coil cell pitch: {cell_pitch:.6f} mm\n")
                f.write(f"# Standalone PCB size: {w:.6f} x {h:.6f} mm\n")
                f.write(f"# Exterior clearance: {float(self.edge_clearance.get()):.6f} mm\n")
                f.write(f"# Nail effective clearance: {tg['nail_effective_clearance']:.6f} mm\n\n")

                # Board outline.
                f.write("LAYER BoardOutline;\n")
                f.write(
                    "LINE 0 "
                    f"(0 0) ({w:.6f} 0) ({w:.6f} {h:.6f}) "
                    f"(0 {h:.6f}) (0 0);\n\n"
                )

                # TOP: bifilar coils only.
                f.write("LAYER Top;\n")
                f.write(line_command(signal, c1.copper, tg['p1']) + "\n")
                f.write(line_command(signal, c1.copper, tg['leads']['c1_inner']) + "\n")
                f.write(line_command(signal, c1.copper, tg['leads']['c1_outer']) + "\n")
                f.write(line_command(signal, c2.copper, tg['p2']) + "\n")
                f.write(line_command(signal, c2.copper, tg['leads']['c2_inner']) + "\n")
                f.write(line_command(signal, c2.copper, tg['leads']['c2_outer']) + "\n\n")

                # PTH vias. Do NOT force 1-16; use Fusion's current default
                # full through-via span to avoid the brief layer-span warning.
                # Fusion-native tented-via fix:
                # Set STOP OFF BEFORE VIA creation so new vias inherit
                # Solder Mask = Off instead of Fusion's newer Auto default.
                f.write("CHANGE STOP OFF;\n")
                f.write(f"CHANGE DRILL {tg['pad_drill_d']:.6f};\n")
                for pad_name, pad_d in (
                    ('c1_inner', tg['inner_pad_d']),
                    ('c2_inner', tg['inner_pad_d']),
                    ('c1_outer', tg['outer_pad_d']),
                    ('c2_outer', tg['outer_pad_d']),
                ):
                    if pad_name == 'c1_outer':  # standalone EXIT terminal
                        pad_d = term['pad_d']
                    f.write(
                        f"VIA '{signal}' {pad_d:.6f} {xy(tg[pad_name])};\n"
                    )

                f.write(f"CHANGE DRILL {tg['bridge_drill_d']:.6f};\n")
                f.write(
                    f"VIA '{signal}' {term['pad_d']:.6f} "
                    f"{xy(tg['bridge_pad'])};\n\n"
                )

                # Bottom routing uses same 3 mm default as the array.
                f.write("LAYER Bottom;\n")
                f.write(
                    line_command(
                        signal, route_w,
                        [tg['c1_inner'], tg['c2_outer']]
                    ) + "\n"
                )
                f.write(
                    line_command(
                        signal, route_w,
                        [tg['c2_inner'], tg['bridge_pad']]
                    ) + "\n\n"
                )

                # Soldermask:
                # tent every via first; then reopen ONLY entry and exit on Top.
                f.write("# PCBWay soldermask: internal vias protected\n")
                for pad_name in (
                    'c1_inner', 'c2_inner', 'c1_outer', 'c2_outer', 'bridge_pad'
                ):
                    f.write(f"CHANGE STOP OFF {xy(tg[pad_name])};\n")

                # Near-circular TOP-only mask openings for standalone ENTRY/EXIT.
                # The opening grows with the terminal copper rim while preserving
                # the same mask overlap used on the normal bridge pads.
                interface_mask_d = term['mask_d']
                interface_half_len = 0.05

                f.write("LAYER tStop;\n")
                for p in (entry, exitp):
                    p1 = (p[0] - interface_half_len, p[1])
                    p2 = (p[0] + interface_half_len, p[1])
                    f.write(
                        f"LINE {interface_mask_d:.6f} {xy(p1)} {xy(p2)};\n"
                    )

                # Center nail hole is NPTH.
                # Minimal board identifier on both silkscreen layers.
                silk_x = 1.50
                silk_y = 0.75
                f.write("LAYER tPlace;\n")
                f.write("CHANGE SIZE 1.000000;\n")
                f.write("CHANGE RATIO 18;\n")
                f.write(f"TEXT 'WYLAR_V1' R0 ({silk_x:.6f} {silk_y:.6f});\n")
                f.write("LAYER bPlace;\n")
                f.write("CHANGE SIZE 1.000000;\n")
                f.write("CHANGE RATIO 18;\n")
                f.write(f"TEXT 'WYLAR_V1' MR0 ({silk_x:.6f} {silk_y:.6f});\n")

                f.write("LAYER Bottom;\n")
                f.write(f"HOLE {tg['nail_d']:.6f} {xy(tg['center'])};\n\n")

                f.write("# EXPOSED STANDALONE INTERFACES ONLY\n")
                f.write(f"# ENTER PAD / NE Out: {xy(entry)}\n")
                f.write(f"# EXIT PAD / C1 Out : {xy(exitp)}\n")

                f.write(
                    "\nDISPLAY Top Bottom Pads Vias BoardOutline Drills Holes tStop bStop;\n"
                )
                f.write("WINDOW FIT;\n")

                # Experimental Fusion bulk via-mask automation.
                # Restrict selection to VIA objects only, group all of them,
                # then apply STOP OFF to the whole group.
                f.write("\n# --- BULK VIA SOLDER MASK OFF ---\n")
                f.write("SET SELECTION_FILTER ON;\n")
                f.write("SET SELECTTYPES NONE VIA;\n")
                f.write("GROUP ALL;\n")
                f.write("CHANGE STOP OFF (> 0 0);\n")
                f.write("GROUP;\n")
                f.write("SET SELECTTYPES ALL;\n")
                f.write("SET SELECTION_FILTER OFF;\n")
                f.write("# --- END BULK VIA SOLDER MASK OFF ---\n")
            messagebox.showinfo(
                'Fusion Single PCB exported',
                f'Saved:\\n{path}\\n\\n'
                f'Auto cell pitch: {cell_pitch:.3f} mm\\n'
                f'PCB size: {w:.3f} × {h:.3f} mm\\n'
                f'Exterior clearance: {float(self.edge_clearance.get()):g} mm\\n'
                f'Nail effective clearance: {tg["nail_effective_clearance"]:.3f} mm\\n'
                f'Bottom routing: {route_w:g} mm\\n\\n'
                'Top: bifilar coils\\n'
                'Bottom: routed series connections\\n'
                'Only ENTRY and EXIT are exposed on Top.\\n'
                'All other vias are soldermask-covered.'
            )

        except Exception as e:
            messagebox.showerror('Fusion single PCB export failed', str(e))


    @staticmethod
    def write_polyline(f, pts, layer):
        def pair(code, val):
            f.write(f'{code}\n{val}\n')

        pair(0, 'POLYLINE')
        pair(8, layer)
        pair(66, 1)
        pair(70, 0)
        for x, y in pts:
            pair(0, 'VERTEX')
            pair(8, layer)
            pair(10, f'{x:.6f}')
            pair(20, f'{y:.6f}')
            pair(30, '0.0')
        pair(0, 'SEQEND')
        pair(8, layer)


if __name__ == '__main__':
    App().mainloop()
