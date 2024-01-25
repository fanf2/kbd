from __future__ import annotations

import copy
from math import copysign, cos, radians, sin, sqrt
from typing import Iterable, Union

from build123d.build_common import WorkplaneList, flatten_sequence, validate_inputs
from build123d.build_enums import AngularDirection, GeomType, LengthMode, Mode
from build123d.build_line import BuildLine
from build123d.geometry import Axis, Plane, Vector, VectorLike
from build123d.objects_curve import BaseLineObject
from build123d.topology import Edge, Face, Wire, Curve

class JernArc(BaseLineObject):
    """JernArc

    Circular tangent arc with given radius and arc_size

    Args:
        start (VectorLike): start point
        tangent (VectorLike): tangent at start point
        radius (float): arc radius
        arc_size (float): arc size in degrees (negative to change direction)
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.

    Attributes:
        start (Vector): start point
        end_of_arc (Vector): end point of arc
        center_point (Vector): center of arc
    """

    _applies_to = [BuildLine._tag]

    def __init__(
        self,
        start: VectorLike,
        tangent: VectorLike,
        radius: float,
        arc_size: float,
        mode: Mode = Mode.ADD,
        plane: Plane = Plane.XY
    ):
        context: BuildLine = BuildLine._get_context(self)
        validate_inputs(context, self)

        start = WorkplaneList.localize(start)
        self.start = start
        start_tangent = WorkplaneList.localize(tangent).normalized()
        if context is None:
            jern_workplane = plane
        else:
            jern_workplane = copy.copy(WorkplaneList._get_context().workplanes[0])
        jern_workplane.origin = start

        arc_direction = copysign(1.0, arc_size)
        self.center_point = start + start_tangent.rotate(
            Axis(start, jern_workplane.z_dir), arc_direction * 90
        ) * abs(radius)
        self.end_of_arc = self.center_point + (start - self.center_point).rotate(
            Axis(start, jern_workplane.z_dir), arc_size
        )
        if abs(arc_size) >= 360:
            circle_plane = copy.copy(jern_workplane)
            circle_plane.origin = self.center_point
            arc = Edge.make_circle(radius, circle_plane)
        else:
            arc = Edge.make_tangent_arc(start, start_tangent, self.end_of_arc)

        super().__init__(arc, mode=mode)
