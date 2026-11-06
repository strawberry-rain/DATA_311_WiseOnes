"""
Humboldt Commute Dashboard (DRAFT v0.2)

Built from the class templates:
  - streamlit_app.py  -> radio buttons with index=None + if/elif branching
  - simple-app.py     -> pandas DataFrame + plotly chart

Pages: Home, Transportation Info, Take the Survey, Explore Data, Useful Links
Everything marked TODO is a placeholder to replace once the design is settled.

Run with:  py -m streamlit run draft_dash.py
    - make sure you are in the Project_2 folder, or adjust the path to draft_dash.py
"""

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Humboldt Commute Dashboard (Draft)",
    page_icon="🚲",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
SECTIONS = [
    "Home",
    "Transportation Info",
    "Take the Survey",
    "Explore Data"
]

st.sidebar.title("Commute Dashboard")
st.sidebar.caption("DRAFT: layout and content will change")
section = st.sidebar.radio("Go to", SECTIONS)


# ---------------------------------------------------------------------------
# Data loading (same idea as the pandas example in simple-app.py)
# ---------------------------------------------------------------------------
@st.cache_data
def load_population():
    # TODO: swap in the full cleaned population file when it's ready
    return pd.read_csv("population_addresses_validated_test_100.csv")


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def render_home():
    st.title("Humboldt Commute Dashboard")
    st.caption("Draft v0.2")

    st.header("Purpose")
    st.info(
        "Should you bring your car when moving to attend Cal Poly Humboldt? "
        "This dashboard is intended to help you figure that out! This page "
        "utilizes three sources of information: "
        "\n1) A commuter survey with synthetic responses, "
            "typically sent out to all students and faculty of Cal Poly Humboldt, "
        "\n2) A synthetic dataset of addresses in the areas where students and faculty typically live."
        "\n3) Routing and transportation data used to calculate commute times from addresses to campus. " 
        "\n\nWhat’s notable about data sets 1 and 2, are that they are artificially produced, "
        "while they represent real life populations, they may not be completely accurate "
        "as to where the actual population lives or real survey answers. "
        "\nTake our survey located on the left to discover the pros " 
        "and cons of bringing a car and help you determine if you should in the first place!"
    )

    st.header("Introduction")
    st.write(
        "Climate Action Analyst Morgan King runs an annual commuter survey of "
        "Cal Poly Humboldt students, faculty, staff and administrators. The "
        "results track commuting patterns and estimate commute-related "
        "greenhouse gas emissions, which are part of the campus carbon footprint."
    )
    st.write(
        "This dashboard builds on that work. TODO: describe what visitors can "
        "do here (try the survey, explore the data, find resources)."
    )

    st.header("Campus commute at a glance")
    st.caption(
        "2025-26 Commuter Report: share of commute trips made by <u>driving alone</u>."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("All campus", "32.0%")
    c2.metric("Students", "26.5%")
    c3.metric("Faculty", "44.1%")
    c4.metric("Staff/Admin", "72.0%")


# ---------------------------------------------------------------------------
# TRANSPORTATION INFO
# ---------------------------------------------------------------------------
def render_transportation():
    st.title("Transportation Info")
    st.write("Ways to get to campus other than driving alone.")

    # (name, description). TODO: confirm details, add costs, hours and routes.
    
    options = [
        (
            "JackPass",
            "Unlimited bus rides, free for students and a small fee for faculty/staff.",
            [
                ("JackPass Website", "https://www.humboldt.edu/transportation-parking/sustainable-transportation/jackpass"),
                ("Bus Schedule and Routes", "https://www.hta.org/")
            ],
        ),
        (
            "Humboldt Bike Share",
            "Bikes available on campus and in the community for discounted rental.",
            [
                ("Humboldt Bike Share", "https://www.tandem-mobility.com/humboldt"),
                ("More Biking Information", "https://www.humboldt.edu/transportation-parking/sustainable-transportation/bike-riding"),
            ],
        ),
        (
            "Bicycle Learning Center",
            "Free bike maintenance and instruction.",
            [
                ("Bicycle Learning Center", "https://www.humboldt.edu/blc"),
                ("More Biking Information", "https://www.humboldt.edu/transportation-parking/sustainable-transportation/bike-riding"),
            ],
        ),
        (
            "Free Ride-match",
            "Connects drivers and riders for carpooling and long-distance trips.",
            [
                ("Visit website", "https://www.humboldt.edu/transportation-parking/sustainable-transportation/carpool-program")
            ],
        ),
        (
            "ZipCar",
            "Cars on demand by the hour or day. ZipCar covers gas, insurance and parking.",
            [
                ("Visit website", "https://www.humboldt.edu/transportation-parking/sustainable-transportation/zipcar")
            ],
        ),
        (
            "Walking",
            "If you live on campus or in Arcata, you can get by without a car. "
            "The University, downtown Arcata, restaurants, shopping centers and health care services are "
            "all within walking distance. Try the Original Mode of Transportation; Be a Pedestrian!",
            [],
        ),
        (
            "Sustainable Transportation",
            "If you want to learn more about transportation options or what the University is doing to promote"
            "sustainable transportation, visit the sustainability dashboard!",
            [
                ("Sustainable Transportation Options", "https://www.humboldt.edu/transportation-parking/sustainable-transportation"),
                ("Sustainability Dashboard", "https://www.humboldt.edu/sustainable-campus/sustainability-dashboard/transportation")
            ]
        )
]

    for name, desc, links in options:
        with st.container(border=True):
            st.subheader(name)
            st.write(desc)
            for label, url in links:
                st.link_button(label, url)  

    st.divider()
    st.subheader("Try it: how far do you live from campus?")
    miles = st.slider("Distance to campus (miles)", 0.0, 30.0, 2.0, 0.5)
    if miles <= 1.5:
        st.success("Walking, biking or transit are all within easy range.")
    elif miles <= 5:
        st.success("Biking, e-biking or the bus are realistic options.")
    elif miles <= 15:
        st.warning("Bus, e-bike or a carpool may fit best. TODO: tailor suggestions.")
    else:
        st.warning("Carpool, ride-match or the express bus may fit best.")
    st.caption("The 2025-26 report counts trips of 1.5 miles or less as walking/biking/transit distance.")


# ---------------------------------------------------------------------------
# SURVEY (branching paths follow the Appendix of the 2025-26 Commuter Report)
# ---------------------------------------------------------------------------
MODES = [
    "Walking (I live on-campus)",
    "Walking (I live off-campus)",
    "Attending virtual classes or telecommuting",
    "Driving alone",
    "University shuttle",
    "Carpool or vanpool with others",
    "Riding the bus",
    "Bicycling, scooter, skateboard or other non-gas mode",
    "Uber or Lyft",
    "Other",
]
DRIVE_MODES = {"Driving alone", "Carpool or vanpool with others"}
BIKE_MODE = "Bicycling, scooter, skateboard or other non-gas mode"

WEEKS = ["<16 (less than one semester)", 
         "16 (one semester)", 
         "32 (two semesters)", 
            "37 (two semesters plus a five-week summer course)", 
            "40 (two semesters plus an eight-week summer course", 
            "42 (two semesters plus two summer courses)", ">42"
]

RESOURCES = [
    "JackPass",
    "Humboldt Bike Share",
    "Bicycle Learning Center",
    "Free Ride-match",
    "ZipCar",
    "Discounted express buses",
]
KNOWLEDGE = [
    "I did not know about it",
    "I did not know, but now I might use it",
    "I knew about it but did not use it",
    "I've used it!",
]


def render_survey():
    st.title("Take the Survey")
    st.caption(
        "DRAFT: a short version of the annual commuter survey. "
        "Answers are not saved anywhere yet, they only show up in this session."
    )

    # --- Q1 housing --------------------------------------------------------
    housing = st.radio(
        "Which best describes where you live?",
        [
            "On-campus University housing",
            "Off-campus University housing (Hinarr Hu Moulik)",
            "Off-campus residence in Humboldt County",
            "Off-campus residence outside Humboldt County",
            "Housing insecure / no consistent place to sleep",
        ],
        index=None,
    )
    if housing is None:
        return

    # --- Q2 days per week --------------------------------------------------
    days = st.select_slider(
        "How many days a week do you commute to the university "
        "(in person or by telecommuting)?",
        options=[1, 2, 3, 4, 5, 6, 7],
        value=5,
    )

    # --- Q3-5: role-specific weeks per year (branch on role) ----------------
    weeks = st.selectbox(
        "Between the end of last May and the end of this May, "
        "about how many weeks will you have come to the university?",
        WEEKS,
        index=None,
    )

    # --- Q6 mode mix (must total 100%) --------------------------------------
    st.subheader("How do you usually get to the university?")
    chosen = st.multiselect("Select every option you typically use", MODES)
    mix = {}
    for mode in chosen:
        mix[mode] = st.number_input(f"% of trips: {mode}", 0, 100, 0, step=5)
    total = sum(mix.values())
    if chosen:
        if total == 100:
            st.success("Total: 100%")
        else:
            st.warning(f"Your percentages add up to {total}%. They need to total 100%.")

    # --- Q7-Q9: follow-ups that only appear for certain answers ------------
    vehicle = charging = bike_type = None

    if any(m in DRIVE_MODES and mix[m] > 0 for m in mix):  # Q8
        vehicle = st.radio(
            "Is your car or motorcycle one of the following?",
            ["Plug-in electric vehicle", "Motorcycle or moped", "Neither"],
            index=None,
        )
        if vehicle == "Plug-in electric vehicle":  # Q9
            charging = st.select_slider(
                "What percentage of your EV charging is done off-campus?",
                options=["0-10%", "11-20%", "21-30%", "31-40%", "41-50%",
                         "51-60%", "61-70%", "71-80%", "81-90%", "91-100%"],
            )

    if mix.get(BIKE_MODE, 0) > 0:  # Q10
        bike_type = st.radio(
            "Is your bike/scooter electric?",
            ["Electric", "Standard, non-electric"],
            index=None,
            horizontal=True,
        )

    # --- Q10 backup mode and barrier ----------------------------------------
    st.subheader("Backup plan")
    backup = st.selectbox(
        "If you couldn't take your primary mode, what would you most likely use?",
        ["Walk", "Carpool/ride with others", "Vanpool", "Uber/Lyft", "Public transit",
         "University shuttle", "Personal non-electric bike or scooter",
         "Personal electric bike or scooter", "Humboldt Bikeshare",
         "Motorcycle/moped", "I have no other option"],
        index=None,
    )
    barrier = None
    if backup and backup != "I have no other option":  # only ask if they have a backup
        barrier = st.radio(
            "What prevents you from using that mode more often?",
            ["Travel time", "Affordability", "Flexibility", "Safety", "Comfort", "Convenience"],
            index=None,
        )

    # --- Q11 location -------------------------------------------------------
    st.subheader("Where you commute from")
    city = st.text_input("City")
    zip_code = st.text_input("Zip code")

    # --- Q12 resource awareness ---------------------------------------------
    st.subheader("Transportation resources")
    resource_answers = {}
    for r in RESOURCES:
        resource_answers[r] = st.selectbox(r, KNOWLEDGE, index=None, key=f"res_{r}")

    # --- Q13 comments ---------------------------------------------------------
    comment = st.text_area("What changes would make it easier to get to campus without a car?")

    # --- Submit ---------------------------------------------------------------
    if st.button("Submit", type="primary"):
        if chosen and total != 100:
            st.error("Please make your mode percentages total 100% before submitting.")
        else:
            st.session_state["last_response"] = {
                "housing": housing, "days_per_week": days,
                "weeks": weeks, "mode_mix": mix, "vehicle": vehicle,
                "ev_offcampus_charging": charging, "bike_type": bike_type,
                "backup_mode": backup, "barrier": barrier, "city": city,
                "zip": zip_code, "resources": resource_answers, "comment": comment,
            }
            st.success("Thanks! Here is what we recorded (TODO: save to a real database).")
            st.json(st.session_state["last_response"])

    # Optional: quick chart of the answer they just gave, like the template's plot
    if mix and total == 100:
        st.subheader("Your commute mix")
        st.bar_chart(pd.Series(mix, name="Percent of trips"))


# ---------------------------------------------------------------------------
# EXPLORE DATA (pandas + plotly, like simple-app.py)
# ---------------------------------------------------------------------------
def render_data():
    st.title("Explore Data")
    st.caption("Sample of 100 student addresses (test file). TODO: use the full cleaned data.")

    df = load_population()

    st.subheader("Sample Data")
    st.dataframe(df[["pop_id", "role", "current_city", "current_zip",
                     "permanent_city", "permanent_state", "permanent_region"]])

    st.subheader("Where students call home")
    counts = df["permanent_region"].value_counts().reset_index()
    counts.columns = ["permanent_region", "students"]
    st.bar_chart(counts.set_index("permanent_region")["students"])

    st.subheader("Where students live now")
    located = df.dropna(subset=["current_lat", "current_lon"])
    st.map(located, latitude="current_lat", longitude="current_lon")
    st.caption(
        f"{len(located)} of {len(df)} addresses could be mapped. "
        "The rest could not be geocoded (cleaning step)."
    )

    st.subheader("Filter")
    city = st.selectbox("Current city", sorted(df["current_city"].dropna().unique()))
    st.write(f"{(df['current_city'] == city).sum()} students in {city}")




#----------------------------------------------------------------------------
RENDERERS = {
    "Home": render_home,
    "Transportation Info": render_transportation,
    "Take the Survey": render_survey,
    "Explore Data": render_data
}
RENDERERS[section]()
