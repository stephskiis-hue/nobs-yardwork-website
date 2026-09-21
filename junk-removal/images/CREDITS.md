# Image credits and licensing

## Stock photography

The following photos came from **Unsplash** (`images.unsplash.com`), which was
the only stock source reachable from the build environment — Pexels and Pixabay
are blocked by the network proxy.

The [Unsplash Licence](https://unsplash.com/license) grants a free, irrevocable,
non-exclusive worldwide copyright licence to use photos **commercially, without
permission or attribution**. Attribution is appreciated but not required, which
is why these are safe on a commercial site.

| File | What the picture actually shows | Used on |
|---|---|---|
| `furniture-removal.webp` | Discarded couches, armchairs and a stripped sofa frame stacked against a shutter | `/furniture-removal-winnipeg` |
| `appliance-removal.webp` | An old rusted refrigerator, door open, standing in long grass | `/appliance-removal-winnipeg` |
| `e-waste.webp` | A dense pile of circuit boards, graphics cards and computer parts | `/e-waste-removal-winnipeg` |
| `renovation-debris.webp` | A steel container heaped with broken tile and demolition debris | `/renovation-debris-removal-winnipeg` |
| `scrap-metal.webp` | Rusted rebar, steel pipe, cable and a perforated plate | `/scrap-metal-removal-winnipeg` |
| `yard-waste.webp` | Cut cedar branches and brush piled on a patio | `/yard-waste-removal-winnipeg` |
| `garage-cleanout.webp` | A garage packed with tools, boxes, a mattress, a smoker and clutter | `/estate-cleanout-winnipeg` |

All seven were opened and visually inspected before use — the description above
is what is actually in the frame, not the search term used to find it. Each was
centre-cropped to 3:2, resized to 1000x667 and saved as WebP at quality 76
(about 111 KB each).

### Known gap: per-photo IDs

The individual Unsplash photo IDs were **not recorded**. The agent doing the
sourcing hit an API rate limit and terminated before writing them down, and its
working notes did not survive. The licence does not require attribution, so
nothing here is out of compliance — but if you ever want to credit the
photographers by name, these seven would need to be re-sourced with their IDs
tracked. Any photo added from here on should have its ID recorded in this table.

### Pexels

Six more photos came from **Pexels** (`images.pexels.com`), added when the
site's own stylesheet replaced the lawn template. The
[Pexels Licence](https://www.pexels.com/license/) allows free commercial use
with no permission or attribution required, and modification is allowed
(these were cropped and re-encoded). What it forbids — selling the photos
unaltered, implying endorsement by the people pictured — this site does not do.

Unlike the Unsplash set, the photo IDs **were** recorded. The photo page is
`https://www.pexels.com/photo/<ID>/`.

| File | Pexels ID | What the picture actually shows | Used on |
|---|---|---|---|
| `junk-hero.webp` | 7464689 | Two workers loading a couch into the back of a white van on a residential street | Homepage hero (and its share image) |
| `hot-tub-removal.webp` | 9899878 | An outdoor hot tub with a weathered wooden cabinet, cover folded back | `/hot-tub-removal-winnipeg` |
| `concrete-removal.webp` | 33484883 | A worker in hi-vis breaking pavement with a jackhammer beside a work truck | `/concrete-removal-winnipeg` |
| `mattress-disposal.webp` | 29348622 | An old mattress and box spring, cropped in tight from a wider rubbish pile | `/mattress-disposal-winnipeg` |
| `piano-removal.webp` | 1021142 | A wooden upright piano against a plain wall | `/piano-removal-winnipeg` |
| `shed-deck-removal.webp` | 3612412 | A weathered grey backyard shed with a broken door leaning against it | `/shed-deck-removal-winnipeg` |

All were opened and looked at before use. The hero is cropped to a 4:5
portrait at 800x1000; the rest are 3:2 at 1000x667. Each category also has a
500x333 tile crop in `images/tiles/`, used by the twelve-tile grid on the
homepage and the What We Take hub; replacing a photo means regenerating its
tile as well.

**The weakest image on the site is `mattress-disposal.webp`.** The wider frame
it came from reads as illegal dumping, which is the opposite of what this
business sells, so it is cropped hard to the mattress. Replace it first when
real job photos exist. All are WebP at quality
72–78, 33–120 KB each. The movers in the hero are models, not No BS crew, and
the alt text says what is in the frame rather than claiming otherwise.

### These are stock, not your jobs

None of these are photographs of No BS work, crew, equipment or customers, and
nothing on the site claims otherwise — there are no captions implying "our
crew" or "a recent job". That matters: presenting stock as your own work is
both dishonest and, for a business selling straight dealing, a bad trade.

**Replacing them with real job photos is the single biggest visual upgrade
available.** Google favours original imagery for local search, and customers can
tell. Drop a replacement in at the same filename and it swaps everywhere with
no other change.

## Original assets (not stock)

`logo.svg`, `footer-logo.svg`, `favicon.webp`, the `icon-take-*.svg` set,
`payments.webp`, crew headshots (`steph-headshot.jpg`, `ben-headshot-min.webp`)
and the job photos carried over from the landscaping side (`skid_steer.webp`,
`snow_removal.webp`, `plow_truck.webp`, `shoveling_snow.webp`) are No-BS's own
property.

The `No-Bs` wordmark inside `logo.svg` is set in **Plus Jakarta Sans ExtraBold**
([SIL Open Font Licence 1.1](https://openfontlicense.org/)), converted to vector
outlines. The OFL permits embedding and redistribution in this form.
