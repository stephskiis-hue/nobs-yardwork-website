"""
_categories.py — everything No BS Junk Removal takes, as data.

WHY THIS IS ITS OWN FILE
------------------------
This list is the single source for every place the site says what we take:
the /what-we-take grid, the /what-we-take-a-z index, the item list on each
category page, the homepage take-list, and the knowsAbout / OfferCatalog /
ItemList structured data. _build.py imports it and generates all of those.

Before it existed, each of those places was written by hand and they had
already drifted: the hub page described ten categories for a site that has
twelve. One list means they cannot disagree.

It lives apart from _build.py because it is pure data and it changes for a
different reason. Adding a service the business now offers should mean
editing a list, not scrolling through build machinery to find the spot.

HOW TO ADD SOMETHING
--------------------
Add an I(...) entry to the right category:

    I("Treadmill", "About 250 to 300 lbs, and ...", aka=["Treadmills"])

  name  — what the thing is called. Shown in the A-Z and on its category page.
  note  — one to three sentences a person could not get from any other junk
          removal site: what makes it awkward, what it weighs, where it goes
          in Winnipeg. If there is nothing true and specific to say, it
          probably belongs as an alias of something else instead.
  aka   — other words people search for the same thing. Each one appears in
          the A-Z as "Loveseat -> see Couch", so the index covers every term
          without writing the same note several times.

Write plain text. Ampersands, quotes and apostrophes are escaped when the
page is rendered, so type "Brick & mortar", not "Brick &amp; mortar".

THE BUILD WILL REFUSE TO RUN IF
-------------------------------
  - the same name or alias appears twice anywhere in this file (case-
    insensitive) — the A-Z would have two entries fighting for one anchor;
  - a category ends up with fewer than MIN_ITEMS real entries;
  - a category's slug has no matching page, or its icon key has no CSS.

WHAT DOES NOT GO IN CATEGORIES
------------------------------
Nothing we cannot legally haul. Those go in NOT_TAKEN at the bottom, each
with where it should go instead. They still appear in the A-Z, marked, so a
person searching for paint disposal lands on a straight answer rather than
nothing — which is the honest version of "we take everything".
"""

MIN_ITEMS = 6


def I(name, note, aka=()):
    return {"name": name, "note": note, "aka": tuple(aka)}


CATEGORIES = [
    # ------------------------------------------------------------------ 1
    {
        "slug": "furniture-removal-winnipeg",
        "icon": "furniture",
        "name": "Furniture & Household",
        "short": "Furniture",
        "blurb": "Couches, beds, tables, carpet and everything else that fills a house.",
        "items": [
            I("Couch",
              "The single most common thing we carry out. A three-seater usually clears a "
              "standard doorway on its end; if it will not, the legs and sometimes the back "
              "come off before we try. Frames with sound upholstery go to reuse first.",
              aka=["Sofa", "Chesterfield", "Loveseat", "Settee", "Davenport"]),
            I("Sectional",
              "Nearly all of them come apart at the connectors, which is how they got into "
              "the room in the first place. Tell us if yours has a recliner or a sofa-bed "
              "module, because those put a lot of weight into one piece.",
              aka=["L-shaped couch", "Modular sofa"]),
            I("Sofa bed",
              "Roughly twice the weight of an ordinary couch because of the steel mechanism "
              "inside. We strap the mechanism shut before it moves so it cannot swing open "
              "on a staircase.",
              aka=["Pull-out couch", "Hide-a-bed"]),
            I("Futon",
              "Frame and mattress come apart and leave separately. Metal futon frames go to "
              "the scrap yard.",
              aka=["Futon frame"]),
            I("Recliner",
              "Power recliners have a motor and wiring, so part of them goes through "
              "electronics recycling. Lift chairs are much heavier than they look; mention "
              "one when you book.",
              aka=["Lift chair", "Power recliner", "Armchair", "Wingback chair"]),
            I("Bed frame",
              "Taken apart if it is still assembled. Metal frames go to scrap and solid wood "
              "ones can often be reused. Mattresses are their own category, and we take both "
              "in the same trip.",
              aka=["Headboard", "Footboard", "Platform bed", "Bunk bed", "Daybed", "Crib"]),
            I("Dresser",
              "Empty the drawers first. A full dresser can weigh twice what an empty one "
              "does, and that weight is time on the stairs. Solid wood pieces in good shape "
              "are offered for reuse before anything else.",
              aka=["Chest of drawers", "Nightstand", "Armoire", "Wardrobe", "Bureau"]),
            I("Dining table",
              "Legs come off wherever they can, which is usually the difference between "
              "getting a table out of a dining room and not. Chair sets in decent condition "
              "are some of the easiest things to rehome.",
              aka=["Kitchen table", "Dining chairs", "Chairs", "Bar stools"]),
            I("Bookcase",
              "Glass doors and shelves come out and travel separately. Particleboard units "
              "rarely survive being moved and go to disposal; solid wood gets offered for "
              "reuse.",
              aka=["Bookshelf", "Shelving unit", "Display cabinet", "China cabinet", "Hutch",
                   "Buffet"]),
            I("Entertainment centre",
              "Old wall-unit entertainment centres are among the heaviest things in a "
              "typical living room, and they rarely fit back through the door they came in "
              "by. They come apart first.",
              aka=["Entertainment center", "TV stand", "Media console", "Wall unit",
                   "Coffee table", "End table", "Side table"]),
            I("Patio furniture",
              "Aluminium and steel frames go to scrap; resin and wicker go to disposal. An "
              "umbrella with a heavy weighted base counts as two things, not one.",
              aka=["Outdoor furniture", "Patio set", "Lawn chairs", "Deck chairs",
                   "Patio umbrella", "Outdoor bench"]),
            I("Office desk",
              "Home-office desks and single workstations. For more than a room's worth of "
              "office furniture, commercial junk removal is set up for exactly that, with "
              "contractor accounts.",
              aka=["Desk", "Computer desk", "Office chair", "Cubicle partition",
                   "Reception desk"]),
            I("Carpet",
              "Rolled and taped before it moves. Wet carpet out of a flooded basement weighs "
              "several times what dry carpet does, so tell us if it is wet.",
              aka=["Rugs", "Area rug", "Underlay", "Carpet padding", "Broadloom"]),
            I("Mirror",
              "Wrapped before it is carried so a crack cannot turn into a hazard halfway "
              "down the stairs.",
              aka=["Wall mirror", "Glass tabletop"]),
            I("Lamp",
              "Fixtures still wired into a ceiling need an electrician to take them down "
              "first. Once they are down, we take them.",
              aka=["Floor lamp", "Light fixture", "Chandelier"]),
            I("Household garbage",
              "Bagged household garbage goes in the trailer like anything else. In most "
              "cleanouts it is the part people most want gone.",
              aka=["Garbage bags", "Trash", "Bagged junk", "Clutter"]),
            I("Clothing",
              "Clean, wearable clothing goes to donation rather than disposal. Curtains and "
              "blinds come down if they are still hanging.",
              aka=["Clothes", "Shoes", "Curtains", "Blinds", "Linens", "Textiles"]),
            I("Books",
              "Books in reasonable condition go to reuse. Personal documents are different: "
              "shred anything with names, addresses or account numbers first. We haul; we do "
              "not shred.",
              aka=["Magazines", "Paper", "Documents"]),
            I("Moving boxes",
              "Break them down and bundle them if you have time, because flat cardboard "
              "takes a fraction of the trailer space and therefore the price. If you do not, "
              "we take them as they are.",
              aka=["Cardboard boxes", "Packing material"]),
            I("Toys",
              "Car seats have an expiry date and should never be reused, so they go to "
              "disposal, not donation. Everything else in good condition is offered for "
              "reuse first.",
              aka=["Kids' toys", "Stuffed animals", "Playpen", "High chair", "Stroller",
                   "Car seat"]),
            I("Home decor",
              "The seasonal decorations of a few decades are a regular part of any basement "
              "or garage cleanout.",
              aka=["Decor", "Picture frames", "Artificial Christmas tree",
                   "Holiday decorations"]),
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "slug": "appliance-removal-winnipeg",
        "icon": "appliance",
        "name": "Appliances & HVAC",
        "short": "Appliances",
        "blurb": "Fridges, washers, stoves, water heaters and furnaces, with refrigerant "
                 "handled properly.",
        "items": [
            I("Fridge",
              "Refrigerant has to be recovered by a certified technician before a fridge is "
              "scrapped, so it goes to a certified recycler and never the landfill. An honest "
              "note first: if yours still works, Efficiency Manitoba will pick it up free and "
              "pay you a $30 rebate. Take that. We will take the dead one.",
              aka=["Refrigerator", "Bar fridge", "Mini fridge", "Wine fridge"]),
            I("Freezer",
              "The same refrigerant rules as a fridge. A chest freezer out of a basement is "
              "one of the more awkward carries in a house, so mention the stairs. Working "
              "units qualify for the same free Efficiency Manitoba pickup and rebate.",
              aka=["Chest freezer", "Deep freeze", "Upright freezer"]),
            I("Stove",
              "Electric ranges we unplug and take. Gas ranges must be disconnected by a "
              "licensed gas fitter before we arrive. That is the law, not our preference.",
              aka=["Range", "Oven", "Wall oven", "Cooktop"]),
            I("Dishwasher",
              "We handle the water line and the drain if you have not. It goes to scrap.",
              aka=["Built-in dishwasher"]),
            I("Washer",
              "Front-loaders carry a concrete counterweight and are far heavier than they "
              "look. We cap the water lines if they are still connected.",
              aka=["Washing machine", "Front-load washer", "Top-load washer",
                   "Stacked washer dryer"]),
            I("Dryer",
              "Electric dryers unplug. Gas dryers need a licensed gas fitter to disconnect "
              "them first. The vent comes out with it.",
              aka=["Clothes dryer"]),
            I("Microwave",
              "Small kitchen appliances go through electronics recycling. Over-the-range "
              "microwaves are bolted to a cabinet and a wall bracket; we take them down.",
              aka=["Over-the-range microwave", "Toaster oven", "Small appliances", "Blender",
                   "Kettle"]),
            I("Range hood",
              "Unbolted and taken as part of a kitchen tear-out.",
              aka=["Exhaust hood", "Stove hood"]),
            I("Air conditioner",
              "Contains refrigerant, so it goes the same certified route as a fridge. Central "
              "air condensers must be disconnected by an HVAC technician before we take them.",
              aka=["Window AC", "Portable AC", "AC unit", "Central air condenser",
                   "Heat pump"]),
            I("Water heater",
              "A 40 or 50 gallon tank weighs far more than people expect once sediment has "
              "settled in the bottom. Drain it if you can. Gas units need a licensed fitter "
              "to disconnect them.",
              aka=["Hot water tank", "Hot water heater", "Tankless water heater"]),
            I("Furnace",
              "Usually removed during a replacement, when your HVAC contractor has already "
              "disconnected it. The steel goes to scrap.",
              aka=["Old furnace", "Boiler", "Ductwork", "HVAC ducting"]),
            I("Dehumidifier",
              "Dehumidifiers contain refrigerant, so they go to a certified recycler rather "
              "than general disposal.",
              aka=["Humidifier", "Air purifier"]),
            I("Water softener",
              "Disconnected and drained, with the salt and resin out before it travels.",
              aka=["Brine tank"]),
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "slug": "mattress-disposal-winnipeg",
        "icon": "mattress",
        "name": "Mattresses & Bedding",
        "short": "Mattresses",
        "blurb": "Every size of mattress and box spring, bagged on site and sent for recycling.",
        "items": [
            I("Mattress",
              "City curbside collection will not take them. We bag every mattress on site "
              "before it moves, and it goes to Mother Earth Recycling on Main Street, "
              "Winnipeg's only mattress recycler, where the steel, foam and fibre are "
              "separated.",
              aka=["Queen mattress", "King mattress", "Double mattress", "Twin mattress",
                   "Single mattress", "Pillow-top mattress"]),
            I("Box spring",
              "A box spring is mostly wood and steel, which is exactly what the recycler "
              "recovers. It goes with the mattress in the same trip.",
              aka=["Boxspring", "Foundation", "Bed base"]),
            I("Memory foam mattress",
              "Awkward rather than heavy: foam flops and will not stay folded. Bagged like "
              "any other.",
              aka=["Foam mattress", "Latex mattress", "Mattress topper"]),
            I("Adjustable bed",
              "The base has motors and wiring, so it goes through electronics and scrap "
              "rather than mattress recycling. Hospital beds are heavy and usually come "
              "apart first.",
              aka=["Adjustable base", "Electric bed base", "Hospital bed"]),
            I("Crib mattress",
              "Small, but still not something the City will take at the curb.",
              aka=["Toddler mattress"]),
            I("Futon mattress",
              "Denser and heavier than it looks. The frame is under Furniture.",
              aka=["Futon pad"]),
            I("Waterbed",
              "It has to be fully drained before we can move it, and that is a job for the "
              "day before, not the day of.",
              aka=["Waterbed mattress"]),
            I("Pillows",
              "Taken as part of a bedroom or full cleanout. Clean bedding in good condition "
              "can be donated.",
              aka=["Bedding", "Duvet", "Comforter", "Sleeping bag"]),
            I("Bed bug mattress",
              "Tell us before we arrive, and we will still take it. It is sealed in plastic "
              "on site so nothing spreads through your hallway or into our trailer, and it "
              "is kept apart from the rest of the load. Most companies in Winnipeg refuse "
              "these outright.",
              aka=["Bed bug infested mattress", "Bed bug furniture", "Infested couch"]),
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "slug": "e-waste-removal-winnipeg",
        "icon": "ewaste",
        "name": "Electronics, TVs & E-Waste",
        "short": "E-Waste & TVs",
        "blurb": "TVs, computers, printers and anything with a circuit board, sent to "
                 "certified recycling.",
        "items": [
            I("Television",
              "Most electronics are banned from Manitoba landfills because of the metals and "
              "flame retardants inside, so every TV goes to certified recycling. Flat screens "
              "are light but fragile, and a cracked panel is a mess to carry.",
              aka=["TV", "Flat screen TV", "LED TV", "LCD TV", "Smart TV"]),
            I("Tube TV",
              "The heaviest, most awkward thing in this category. A 32-inch tube set can "
              "pass 100 lbs, and rear-projection sets are the size of furniture. These are "
              "exactly the reason people call instead of dealing with it themselves.",
              aka=["CRT TV", "CRT television", "Old TV", "Big screen TV",
                   "Rear projection TV", "Console TV"]),
            I("Plasma TV",
              "Heavier than an LED set of the same size, with a glass panel that does not "
              "like being flexed. It is carried upright.",
              aka=["Plasma television"]),
            I("Computer",
              "Pull the hard drive before we take it, or destroy it. We do not wipe drives, "
              "and you should not assume anyone later in the chain will either. That is the "
              "only data advice we can actually stand behind.",
              aka=["Desktop computer", "Laptop", "Tower", "PC", "Mac", "Server"]),
            I("Monitor",
              "Goes with the computer to certified e-waste recycling.",
              aka=["Computer monitor", "Screen"]),
            I("Printer",
              "Office copiers are heavy and ride on casters that were never built for "
              "stairs. Pull any toner cartridges you want to recycle separately.",
              aka=["Scanner", "Copier", "Photocopier", "Fax machine", "All-in-one printer"]),
            I("Stereo",
              "Big floor speakers are mostly wood and magnet, and weigh accordingly.",
              aka=["Speakers", "Receiver", "Amplifier", "Subwoofer", "Record player",
                   "Turntable"]),
            I("DVD player",
              "Small and light, and all of it goes to certified e-waste recycling rather "
              "than general disposal.",
              aka=["VCR", "Blu-ray player", "Cable box", "Satellite receiver", "Projector",
                   "Game console"]),
            I("Cables",
              "The tangle in the drawer. Bag it and it goes with everything else.",
              aka=["Cords", "Wires", "Keyboard", "Mouse", "Chargers", "Power bars",
                   "Remotes"]),
            I("Cell phone",
              "Take out the SIM card and factory-reset the device first. The battery inside "
              "goes to the proper recycling stream.",
              aka=["Cell phones", "Smartphone", "Tablet", "Old phones"]),
            I("Satellite dish",
              "Taken down if it is still mounted, as long as it can be reached safely from "
              "a ladder. Roof work beyond that needs someone with fall protection.",
              aka=["TV antenna", "Antenna", "TV dish"]),
            I("TV wall mount",
              "Unbolted and taken with the TV. We leave the anchors in the wall unless you "
              "ask otherwise.",
              aka=["TV bracket", "Wall bracket"]),
            I("Light bulbs",
              "Fluorescent tubes and compact fluorescents contain a little mercury, so they "
              "need to arrive unbroken. Keep them in their boxes or tape them together. They "
              "go to proper recycling, not loose on the trailer floor.",
              aka=["CFL bulbs", "Fluorescent tubes", "LED bulbs"]),
            I("Household batteries",
              "Bag them, and tape the ends of any lithium or 9-volt batteries so they cannot "
              "short. Swollen or leaking batteries are a different matter: call us first.",
              aka=["AA batteries", "Rechargeable batteries"]),
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "slug": "renovation-debris-removal-winnipeg",
        "icon": "reno",
        "name": "Renovation & Demolition Debris",
        "short": "Reno Debris",
        "blurb": "Drywall, lumber, flooring, shingles and full interior demolition.",
        "items": [
            I("Drywall",
              "Among the most common renovation materials, and heavier per load than people "
              "expect. Joint compound in older homes can contain asbestos, so if you are "
              "unsure, have it tested before demolition rather than after.",
              aka=["Gypsum board", "Sheetrock", "Gyprock"]),
            I("Lumber",
              "Pull the nails if you have time, but you do not have to. Wood over four "
              "inches thick tips at its own rate at Brady Road, which is one reason we sort "
              "loads.",
              aka=["Wood", "Framing lumber", "2x4s", "Plywood", "OSB", "Trim", "Baseboards"]),
            I("Pallets",
              "Stacked flat they take a fraction of the space they do thrown in loose, and "
              "space is what you pay for.",
              aka=["Wood pallets", "Skids"]),
            I("Flooring",
              "Pulled up and hauled. Old sheet vinyl and the black mastic under it can "
              "contain asbestos in older Winnipeg homes, so test before tearing it out.",
              aka=["Laminate", "Hardwood flooring", "Vinyl flooring", "Linoleum", "Subfloor"]),
            I("Tile",
              "Heavy for its volume, so larger tile jobs are priced by weight rather than "
              "trailer space.",
              aka=["Ceramic tile", "Porcelain tile", "Backsplash"]),
            I("Shingles",
              "Priced by weight. A full roof tear-off runs to several tonnes and suits "
              "repeated loads; a garage roof or a partial is exactly our size of job.",
              aka=["Roofing", "Asphalt shingles", "Roof tear-off"]),
            I("Insulation",
              "Bagged before it moves so it does not shed through the house. Loose, "
              "grey-brown, pebbly vermiculite can contain asbestos and must be tested first. "
              "We cannot take it until it has been.",
              aka=["Batt insulation", "Fibreglass insulation", "Rigid foam insulation"]),
            I("Plaster",
              "Priced by weight. Common in Winnipeg homes built before the 1950s, which is "
              "also why it is worth an asbestos test before a wall comes down.",
              aka=["Plaster and lathe", "Lath", "Horsehair plaster"]),
            I("Ceiling tile",
              "Older ceiling tiles are another material worth testing for asbestos before "
              "they come down.",
              aka=["Drop ceiling", "Acoustic tile", "Ceiling panels"]),
            I("Doors",
              "Solid doors in good condition are good reuse candidates.",
              aka=["Interior doors", "Exterior doors", "Closet doors", "Storm doors"]),
            I("Windows",
              "The glass is wrapped before it is carried.",
              aka=["Old windows", "Window frames", "Storm windows"]),
            I("Kitchen cabinets",
              "Removed and hauled in one visit during a kitchen or bathroom tear-out. Stone "
              "countertops are heavy enough to have their own entry under heavy awkward "
              "items.",
              aka=["Cabinets", "Bathroom vanity", "Vanity", "Laminate countertop"]),
            I("Siding",
              "Aluminium siding and trim go to scrap; vinyl goes to disposal.",
              aka=["Vinyl siding", "Aluminium siding", "Soffit", "Fascia"]),
            I("Construction cardboard",
              "The mountain of packaging a renovation leaves behind. Flattened, it takes "
              "surprisingly little room.",
              aka=["Bulk cardboard", "Appliance boxes"]),
            I("Bathtub",
              "Acrylic and fibreglass tubs and shower stalls are light. Cast iron tubs are a "
              "very different job and have their own entry under heavy awkward items.",
              aka=["Tub", "Shower stall", "Shower surround", "Toilet", "Sink"]),
            I("Interior demolition",
              "We do the tear-out as well as the haul-away: non-structural walls, kitchens, "
              "bathrooms and basements. Anything load-bearing needs an engineer and a permit "
              "first, and in an older home asbestos testing comes before any of it.",
              aka=["Demolition", "Demo", "Kitchen demolition", "Bathroom demolition",
                   "Basement demolition", "Gutting a room"]),
            I("Flood cleanup",
              "Soaked drywall, carpet and furniture out of a flooded basement. Anything "
              "contaminated by sewage or significant mould needs a remediation company "
              "involved, and we will say so plainly if that is where it has got to.",
              aka=["Water damage cleanup", "Sewer backup cleanup", "Fire cleanup",
                   "Disaster cleanup"]),
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "slug": "hot-tub-removal-winnipeg",
        "icon": "hot-tub",
        "name": "Hot Tubs, Spas & Pools",
        "short": "Hot Tubs",
        "blurb": "Hot tubs, swim spas and above-ground pools, cut down and hauled in one visit.",
        "items": [
            I("Hot tub",
              "Usually 500 to 900 lbs empty, and nearly always behind a gate narrower than "
              "the tub. It gets cut into sections on site, which is normal and included. We "
              "disconnect at the whip; anything at the panel is an electrician's job.",
              aka=["Spa", "Jacuzzi", "Portable spa", "Outdoor hot tub"]),
            I("Swim spa",
              "Much larger and heavier than a hot tub, often twice the length. Access is the "
              "whole question, so we look before we quote.",
              aka=["Exercise pool", "Endless pool"]),
            I("Hot tub cover",
              "A waterlogged cover can weigh several times what it did new.",
              aka=["Spa cover"]),
            I("Above-ground pool",
              "Drained, dismantled and hauled: walls, frame and liner. The steel walls go to "
              "scrap. The ground underneath usually needs levelling and seeding afterwards, "
              "which is exactly the kind of work our landscaping side does.",
              aka=["Pool", "Swimming pool", "Round pool", "Oval pool"]),
            I("Pool equipment",
              "Taken with the pool or on their own.",
              aka=["Pool liner", "Pool filter", "Pool pump", "Pool heater", "Pool ladder",
                   "Pool cover"]),
            I("Gazebo",
              "Taken down and hauled. Cedar and aluminium frames go to different streams.",
              aka=["Pergola", "Hot tub enclosure", "Screen house", "Canopy"]),
            I("Playhouse",
              "Plastic playhouses come apart. Wooden ones are taken down like a small shed.",
              aka=["Kids' playhouse", "Cubby house"]),
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "slug": "shed-deck-removal-winnipeg",
        "icon": "shed",
        "name": "Sheds, Decks, Fences & Garages",
        "short": "Sheds & Decks",
        "blurb": "Teardown and haul-away of sheds, decks, fences, garages and backyard "
                 "structures.",
        "items": [
            I("Shed",
              "Torn down and hauled in one visit, with metal sheds going to scrap. If the "
              "floor sits on a concrete pad, say so: the pad is priced by weight and belongs "
              "in the quote, not in a surprise.",
              aka=["Garden shed", "Storage shed", "Tool shed", "Metal shed"]),
            I("Deck",
              "Boards, joists, railings and stairs. Winter is genuinely the gentlest time to "
              "take a deck out, because frozen ground does not rut under the weight.",
              aka=["Wood deck", "Composite deck", "Deck boards", "Porch", "Deck stairs"]),
            I("Deck footings",
              "Come out with the skid steer. They are concrete, so they are priced by weight.",
              aka=["Concrete footings", "Sonotubes", "Piles", "Post bases"]),
            I("Fence",
              "Posts come out with the concrete plug still attached. Leaving broken posts in "
              "the ground is how the next person to build a fence ends up with a bad day.",
              aka=["Wood fence", "Privacy fence", "Picket fence", "Fence panels"]),
            I("Chain link fence",
              "The mesh and the posts go to scrap.",
              aka=["Chain-link", "Wire fence", "Metal fence", "Dog run", "Kennel"]),
            I("Detached garage",
              "A garage teardown is a structural demolition and usually needs a City of "
              "Winnipeg permit, which is on the property owner. The slab comes out separately "
              "and is priced by weight.",
              aka=["Garage", "Carport"]),
            I("Retaining wall",
              "Old railway ties are treated with creosote and cannot go in regular disposal "
              "or be burned. Block walls are heavy material, priced by weight.",
              aka=["Timber retaining wall", "Landscape ties", "Railway ties"]),
            I("Trampoline",
              "The frame is galvanized steel and goes to scrap; the mat and net go to "
              "disposal. Taken apart on site.",
              aka=["Trampoline frame", "Trampoline net"]),
            I("Playset",
              "Wooden playsets are a small demolition, not a lift: they are bolted together "
              "and often set in the ground. Metal swing sets go to scrap.",
              aka=["Swing set", "Play structure", "Playground", "Climbing frame", "Slide"]),
            I("Basketball hoop",
              "Portable hoops have a base full of sand or water that has to be emptied first. "
              "In-ground poles set in concrete come out with the skid steer.",
              aka=["Basketball net", "Portable hoop", "In-ground hoop"]),
            I("Greenhouse",
              "Glass panels are wrapped; polycarbonate and the frame are sorted separately.",
              aka=["Cold frame", "Polytunnel"]),
            I("Flagpole",
              "Cut down or pulled, including the concrete base.",
              aka=["Clothesline", "Clothesline pole"]),
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "slug": "concrete-removal-winnipeg",
        "icon": "concrete",
        "name": "Concrete, Dirt & Heavy Material",
        "short": "Concrete & Brick",
        "blurb": "Concrete, brick, dirt, gravel and anything priced by the tonne.",
        "items": [
            I("Concrete",
              "Broken out with the skid steer and hauled the same visit. Keep it clean, with "
              "no rebar mesh, wood or dirt through it, and it tips at $11.30 a tonne at "
              "Brady Road instead of $99. That difference comes straight off your price.",
              aka=["Concrete slab", "Driveway", "Sidewalk", "Patio pad", "Broken concrete"]),
            I("Brick",
              "Heavy and dense. Clean brick is priced at the clean concrete rate.",
              aka=["Bricks", "Chimney brick", "Brick pavers"]),
            I("Patio stones",
              "Lifted and hauled. The sand and gravel base underneath is its own line in the "
              "quote if it is coming out too.",
              aka=["Pavers", "Patio slabs", "Paving stones", "Interlocking brick", "Flagstone"]),
            I("Asphalt",
              "Priced by weight, like concrete.",
              aka=["Blacktop", "Asphalt driveway"]),
            I("Gravel",
              "Landscape rock is one of the heaviest things we are asked to move for the "
              "space it takes. Tell us roughly how deep it is laid and we can estimate the "
              "tonnage before we arrive.",
              aka=["Crushed stone", "Rock", "River rock", "Landscape rock", "Pea gravel"]),
            I("Dirt",
              "Clean fill tips at $9 a tonne at Brady Road, which makes clean dirt one of the "
              "least expensive heavy loads to dispose of. Winnipeg clay is dense and wet, and "
              "weighs more than dry soil.",
              aka=["Soil", "Topsoil", "Clay", "Fill", "Excavation spoil"]),
            I("Sand",
              "Priced by weight.",
              aka=["Sandbox sand", "Play sand", "Bedding sand"]),
            I("Cinder blocks",
              "Priced by weight, and at the clean concrete rate if they are clean.",
              aka=["Concrete blocks", "Retaining wall blocks", "Landscape blocks"]),
            I("Stone",
              "Large decorative boulders need the skid steer. Priced by weight.",
              aka=["Natural stone", "Boulders", "Fieldstone"]),
            I("Stucco",
              "Priced by weight as mixed heavy material, since it is usually bonded to lath "
              "and wire mesh that cannot be separated from it.",
              aka=["Parging"]),
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "slug": "yard-waste-removal-winnipeg",
        "icon": "yard",
        "name": "Yard Waste & Seasonal",
        "short": "Yard Waste",
        "blurb": "Branches, brush, leaves, sod, stumps and storm cleanup.",
        "items": [
            I("Branches",
              "City yard waste collection only takes branches under 10 cm across and a metre "
              "long, bundled. Anything bigger, or a whole pile of it, is where we come in.",
              aka=["Tree branches", "Limbs", "Deadfall"]),
            I("Brush",
              "A torn-out cedar hedge is dense and springy, and takes far more trailer space "
              "than it looks like it will on the lawn. Cut it into lengths if you can.",
              aka=["Brush pile", "Shrubs", "Bushes", "Hedge", "Hedge trimmings", "Cedar hedge"]),
            I("Leaves",
              "City collection takes leaves in paper bags only, never plastic. If you have a "
              "garage full of them in the wrong bags, we take them anyway.",
              aka=["Leaf bags", "Fall leaves"]),
            I("Grass clippings",
              "Heavy when wet. Taken as part of a yard cleanup.",
              aka=["Lawn clippings", "Thatch"]),
            I("Garden waste",
              "Pulled plants, spent garden beds and old mulch. It goes to composting rather "
              "than the landfill.",
              aka=["Plants", "Weeds", "Perennials", "Mulch"]),
            I("Sod",
              "Priced by weight, because a roll of wet sod is mostly soil and water. Common "
              "when a lawn is being replaced with a patio or garden.",
              aka=["Turf", "Old sod", "Lawn removal"]),
            I("Stumps",
              "We haul stumps that have already been cut or ground out. Pulling a large stump "
              "out of the ground is a job for a stump grinder, and we will tell you so rather "
              "than guess at it.",
              aka=["Tree stumps", "Roots", "Root ball"]),
            I("Tree debris",
              "We take the cut pieces once a tree is down. Bringing a standing tree down is "
              "an arborist's job. Wood over four inches thick tips at its own rate at Brady.",
              aka=["Logs", "Firewood", "Tree trunks", "Cut tree"]),
            I("Storm debris",
              "After a big storm the whole city calls at once, so call early. We clear what "
              "came down; anything still hanging over a roof or a line needs an arborist "
              "first.",
              aka=["Storm damage", "Fallen tree", "Wind damage"]),
            I("Christmas tree",
              "Stripped of lights and tinsel first. The City runs its own tree collection "
              "each January. If you missed it, or the tree has sat frozen in the yard until "
              "April, we will take it.",
              aka=["Real Christmas tree", "Live Christmas tree"]),
            I("Planters",
              "Empty them first if you can. Heavy clay and concrete planters are priced by "
              "weight.",
              aka=["Flower pots", "Garden pots", "Raised garden beds", "Garden boxes"]),
            I("Compost bin",
              "Plastic compost bins and rain barrels go with a yard cleanup.",
              aka=["Rain barrel"]),
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "slug": "estate-cleanout-winnipeg",
        "icon": "estate",
        "name": "Estate, Hoarding & Cleanouts",
        "short": "Estate Cleanouts",
        "blurb": "Whole houses, garages, basements and storage units, at your pace.",
        "items": [
            I("Estate cleanout",
              "Whole houses cleared at the pace the family needs. Anything you flag is set "
              "aside rather than thrown out, paperwork and photographs go in one place, and "
              "we send photos on completion if you need them for the estate.",
              aka=["Estate clearance", "Clearing a parent's house", "Probate cleanout"]),
            I("Hoarding cleanup",
              "Handled without commentary, at a pace the person involved can manage. If "
              "there is significant biohazard, mould or pest infestation, a remediation "
              "company needs to be involved too, and we will say so plainly rather than make "
              "it worse.",
              aka=["Hoarder house", "Hoarding cleanout"]),
            I("Garage cleanout",
              "The accumulation of a decade, usually gone in a morning. You point at what "
              "stays and we take the rest.",
              aka=["Garage cleanup", "Garage clearout"]),
            I("Basement cleanout",
              "Habitat for Humanity's ReStore will not go into basements for donation "
              "pickups. We will, and anything worth donating we set aside for you.",
              aka=["Basement cleanup", "Basement clearout", "Crawl space"]),
            I("Attic cleanout",
              "Narrow hatches and pull-down ladders make attics slow work. Tell us what the "
              "access is like when you book.",
              aka=["Attic cleanup", "Loft"]),
            I("Storage unit cleanout",
              "Emptied and swept so you can hand the keys back. Let the facility know we are "
              "coming, since some keep a list of who is allowed in.",
              aka=["Storage locker", "Self-storage unit"]),
            I("Rental cleanout",
              "Whatever a tenant left behind, cleared before the next one moves in, with "
              "photos on completion for your records.",
              aka=["Landlord turnover", "Tenant left junk", "Eviction cleanout",
                   "Apartment cleanout", "Move-out cleanout"]),
            I("Foreclosure cleanout",
              "Cleared and documented for realtors and property managers.",
              aka=["Bank-owned property", "Vacant property"]),
            I("Downsizing",
              "Moving from a family home to somewhere smaller usually means deciding about "
              "decades of belongings in a few weeks. We work to your moving date, and "
              "seniors get 10% off.",
              aka=["Senior downsizing", "Moving to a condo", "Moving to a retirement home"]),
            I("Whole house cleanout",
              "Every room, top to bottom, in as many trips as it takes, priced by the trailer "
              "loads it fills.",
              aka=["Full house clearout", "House clearance"]),
        ],
    },
    # ------------------------------------------------------------------ 11
    {
        "slug": "scrap-metal-removal-winnipeg",
        "icon": "scrap",
        "name": "Scrap Metal, Tires & Auto",
        "short": "Scrap Metal",
        "blurb": "Scrap metal, gym equipment, lawnmowers, tires and auto parts.",
        "items": [
            I("Scrap metal",
              "If the whole load is metal and there is enough of it, the scrap value can "
              "cover some or all of the job. A single rusty item will not, but it costs "
              "nothing to ask.",
              aka=["Metal", "Steel", "Aluminium", "Aluminum", "Copper", "Iron"]),
            I("Lawnmower",
              "Drain the gas and oil first, or tell us you have not. The engine and deck go "
              "to scrap.",
              aka=["Lawn mower", "Riding mower", "Push mower", "Lawn tractor", "Weed trimmer"]),
            I("Snowblower",
              "Same as a mower: drain the fuel. Most of it is steel.",
              aka=["Snow blower", "Snowthrower"]),
            I("BBQ",
              "We take the barbecue, but not the propane tank attached to it. Disconnect the "
              "tank first and take it to a propane exchange or a 4R Depot.",
              aka=["Barbecue", "Grill", "Gas grill", "Charcoal grill", "Smoker"]),
            I("Bicycle",
              "Bikes in rideable condition go to reuse programs rather than scrap.",
              aka=["Bike", "Kids' bike", "Tricycle", "Scooter"]),
            I("Treadmill",
              "About 250 to 300 lbs, and the deck folds but the frame does not. A basement "
              "treadmill is a two-person carry with stair gear. The steel frame goes to scrap, "
              "so a load of gym equipment often prices like an all-metal load.",
              aka=["Treadmills"]),
            I("Exercise equipment",
              "Mostly steel, which means it is heavy and it is scrap-yard material. Home gyms "
              "with a weight stack come apart before they move.",
              aka=["Elliptical", "Stationary bike", "Exercise bike", "Home gym",
                   "Weight bench", "Rowing machine", "Stair climber"]),
            I("Free weights",
              "Small, dense and heavy. Cast iron plates go straight to scrap.",
              aka=["Dumbbells", "Barbells", "Weight plates", "Kettlebells"]),
            I("Filing cabinet",
              "Empty the drawers first. A full four-drawer cabinet is more weight than two "
              "people should be carrying.",
              aka=["File cabinet", "Metal cabinet", "Metal shelving", "Lockers"]),
            I("Eavestrough",
              "Aluminium and steel both go to scrap.",
              aka=["Gutters", "Downspouts", "Metal roofing"]),
            I("Radiator",
              "Old cast iron radiators are remarkably heavy for their size, and some pass "
              "300 lbs. They go to scrap.",
              aka=["Cast iron radiator", "Hot water radiator", "Pipe", "Copper pipe",
                   "Cast iron pipe"]),
            I("Tires",
              "They go through the Tire Stewardship Manitoba network rather than the "
              "landfill. Tires on rims are fine; the rim is scrap anyway.",
              aka=["Tire", "Car tires", "Truck tires", "Tires on rims", "Winter tires"]),
            I("Car parts",
              "Drained of fluids first. We take parts, not whole vehicles: a car needs a "
              "licensed auto recycler who can handle the fluids and the ownership transfer.",
              aka=["Auto parts", "Engine parts", "Rims", "Transmission", "Car doors"]),
            I("Car battery",
              "Intact, upright and not leaking, and it goes to recycling. A cracked or "
              "leaking battery is hazardous and belongs at a 4R Depot, which takes them free.",
              aka=["Car batteries", "Lead acid battery", "Truck battery"]),
        ],
    },
    # ------------------------------------------------------------------ 12
    {
        "slug": "piano-removal-winnipeg",
        "icon": "piano",
        "name": "Pianos & Heavy Awkward Items",
        "short": "Pianos",
        "blurb": "Pianos, safes, pool tables and anything too heavy for two people.",
        "items": [
            I("Upright piano",
              "400 to 800 lbs, almost all of it the cast iron plate inside, and the wrong "
              "technique breaks a foot, a floor or a stair tread. Before paying to move one, "
              "know that most old uprights have no resale or donation value.",
              aka=["Piano", "Spinet piano", "Console piano", "Studio piano"]),
            I("Grand piano",
              "Legs and lyre come off, and the body travels on its side on a piano board. A "
              "full grand can pass 1,000 lbs.",
              aka=["Baby grand", "Baby grand piano"]),
            I("Organ",
              "Heavy, and electric organs go through electronics recycling as well.",
              aka=["Electric organ", "Church organ", "Pump organ"]),
            I("Pool table",
              "A slate table is three slabs of stone totalling several hundred pounds. It "
              "comes apart first, and the slate is the heavy part.",
              aka=["Billiard table", "Snooker table", "Slate pool table"]),
            I("Safe",
              "Tell us the size and whether it is bolted down. Gun safes can pass 500 lbs and "
              "must be empty, and we need to know that before we arrive.",
              aka=["Gun safe", "Fireproof safe", "Floor safe"]),
            I("Cast iron tub",
              "300 lbs or more, usually on the second floor of an old house. Sometimes the "
              "fastest safe way out is in pieces.",
              aka=["Clawfoot tub", "Cast iron bathtub", "Cast iron sink"]),
            I("Arcade cabinet",
              "Heavy, top-heavy and full of electronics. The glass comes out before it moves.",
              aka=["Arcade machine", "Pinball machine", "Jukebox"]),
            I("Vending machine",
              "Commercial refrigeration contains refrigerant and goes the certified route. "
              "These usually need a freight path and a pallet jack.",
              aka=["Pop machine", "Commercial freezer", "Commercial fridge", "Walk-in cooler"]),
            I("Commercial kitchen equipment",
              "Gas equipment has to be disconnected by a licensed fitter first, and deep "
              "fryers must be drained of oil.",
              aka=["Restaurant equipment", "Commercial range", "Deep fryer",
                   "Commercial dishwasher"]),
            I("Granite slab",
              "Stone countertops are carried on edge because they are brittle across their "
              "length. Priced by weight.",
              aka=["Granite countertop", "Stone countertop", "Marble slab",
                   "Quartz countertop"]),
            I("Grandfather clock",
              "The weights and pendulum come out first so nothing swings loose on the way "
              "down.",
              aka=["Longcase clock"]),
            I("Aquarium",
              "Completely empty and dry first. A large tank is heavy glass and awkward to "
              "carry.",
              aka=["Fish tank", "Terrarium"]),
            I("Church pews",
              "Long, solid and heavy, and usually leaving a building with a tight corner "
              "somewhere on the way out.",
              aka=["Pews", "Long benches"]),
        ],
    },
]


# Terms people search for that are services rather than things. They appear in
# the A-Z pointing at the service page, so nothing searchable is orphaned.
SERVICE_TERMS = [
    {"name": "Office cleanout", "slug": "commercial-junk-removal-winnipeg",
     "note": "Office, retail and warehouse cleanouts run through commercial junk removal, "
             "with contractor accounts and scheduling around business hours.",
     "aka": ("Office furniture removal", "Business cleanout", "Retail cleanout",
             "Store cleanout", "Warehouse cleanout")},
    {"name": "Job site cleanup", "slug": "commercial-junk-removal-winnipeg",
     "note": "Construction debris and lot cleanups with the skid steer and dump trailer, "
             "including repeat pickups on a schedule that suits the build.",
     "aka": ("Construction site cleanup", "Lot cleanup", "Commercial lot cleanup")},
    {"name": "Snow removal", "slug": "winter-services-winnipeg",
     "note": "Snow clearing and off-site snow hauling through the winter, when the rest of "
             "the hauling work slows down.",
     "aka": ("Snow hauling", "Snow clearing")},
]


# Things we cannot legally haul, and where each one should go instead. These
# drive the /what-we-dont-take page and appear in the A-Z, marked, so a search
# for any of them still reaches a straight answer.
#
# "where" must be a real Winnipeg route. The City runs three 4R Winnipeg Depots
# for residents: Brady (1825 Brady Rd), Pacific (1120 Pacific Ave) and Panet
# (429 Panet Rd); Pacific and Panet are closed Wednesdays. They do not all
# accept the same things, which is why the copy says "a 4R Depot" and sends
# people to the City's page rather than claiming a particular one takes it.
# Re-check against winnipeg.ca before changing any of these.
NOT_TAKEN = [
    {"name": "Paint",
     "why": "Liquid paint, stains and solvents are household hazardous waste.",
     "where": "A 4R Winnipeg Depot takes them free for Winnipeg residents. Fully dried-out "
              "latex paint cans are a different case, so ask us.",
     "aka": ("Paint cans", "Stain", "Varnish", "Paint thinner", "Solvents")},
    {"name": "Propane tank",
     "why": "Pressurized cylinders can rupture in a loaded trailer.",
     "where": "Swap it at a propane exchange, or take it to a 4R Winnipeg Depot.",
     "aka": ("Propane cylinder", "BBQ propane tank", "Compressed gas cylinder")},
    {"name": "Asbestos",
     "why": "Removing or hauling it without licensing is illegal and genuinely dangerous.",
     "where": "Have suspect material tested first, then use a licensed abatement "
              "contractor. We are glad to haul everything else once it is cleared.",
     "aka": ("Vermiculite insulation", "Suspected asbestos")},
    {"name": "Chemicals",
     "why": "Pesticides, pool chemicals and cleaners are household hazardous waste.",
     "where": "A 4R Winnipeg Depot takes them free for Winnipeg residents.",
     "aka": ("Pesticides", "Herbicides", "Pool chemicals", "Aerosol cans")},
    {"name": "Motor oil",
     "why": "Fuel, oil and antifreeze are hazardous and flammable.",
     "where": "A 4R Winnipeg Depot takes them free for Winnipeg residents.",
     "aka": ("Used oil", "Antifreeze", "Gasoline", "Fuel")},
    {"name": "Medical waste",
     "why": "Sharps and biohazard waste need controlled handling.",
     "where": "Most pharmacies take back sharps containers and unused medication.",
     "aka": ("Sharps", "Needles", "Syringes", "Biohazard waste")},
    {"name": "Ammunition",
     "why": "Ammunition, fireworks and explosives cannot go in a trailer.",
     "where": "Call the Winnipeg Police Service non-emergency line and ask about safe "
              "disposal.",
     "aka": ("Explosives", "Fireworks", "Flares")},
    {"name": "Vehicles",
     "why": "A vehicle needs its fluids handled and its ownership transferred properly.",
     "where": "Use a licensed auto recycler. We take car parts, tires and intact batteries.",
     "aka": ("Car", "Truck", "Junk car", "Scrap car")},
]
