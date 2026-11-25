---
name: room-layout
description: "Compare room arrangements using measured dimensions and a scaled floor plan."
---

# Room layout

Compare room arrangements using measured dimensions and a scaled floor plan.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Record dimensions, fixed openings, door swing, furniture footprints and the user's required clearance in one unit.
2. Draw the room to scale. Make two placements and mark the narrowest gap with furniture in use.
3. Check the path from door to chair in each layout. Label unknown wall or window dimensions and list the measurements needed on site.

## Try it

Place a 1.2 by 0.6 metre desk in a 3 by 4 metre study with an inward-opening door.

**Expected result.** Two scaled placements with the clearance, door swing and limiting measurement marked.

Reserve a 0.8 m square for a doorway in the corner of the plan. A desk whose rectangle intersects it needs to move even when the desk itself lies inside the room.

**Limit.** Concept planning only. Site measurements and applicable building requirements need independent verification.

## Draw and check a floor plan

Run `python3 plan.py study.json study.svg` from this directory, choosing a new output filename. The [example](study.json) uses metres and rectangles in x, y, width, depth order. Origin is the upper-left corner. Include clearance regions as rectangles when they need to remain empty. A rectangle is a conservative approximation of a door sweep.

The sample yields zero overlap or boundary findings. Move the desk to x = 0 and compare the second SVG and overlap message. Exit 0 means no detected conflict, 1 means a geometry finding and 2 means an input or output error. The checker handles axis-aligned rectangles only.

## Draw connected rooms

For several rooms or levels, use the measured [two-room model](two-rooms.json). From this skill directory run `python3 floor_plan.py two-rooms.json drawing`, where `drawing` is a new output directory. It contains a scaled SVG per level, a room and opening schedule, and a structured scene in metres. The example has two adjoining rooms and seven wall segments, including one shared interior wall.

The site lot and each rectangular room use x, y, width and depth. Room IDs must be unique within a level. Adjacent rooms share the coordinates of their common wall centerline. The scene records wall segments, openings, room boundaries, levels and camera positions. Inspect the SVG and schedule before using the geometry in another tool. The scene JSON is a structured interchange file and needs a separate viewer for a photorealistic render.
