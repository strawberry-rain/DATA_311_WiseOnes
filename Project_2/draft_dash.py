"""
Humboldt Commute Dashboard (DRAFT v0.2)

Built from the class templates:
  - streamlit_app.py  -> radio buttons with index=None + if/elif branching
  - simple-app.py     -> pandas DataFrame + plotly chart

Pages: Home, Transportation Info, Take the Survey, Explore Data, Useful Links
Everything marked TODO is a placeholder to replace once the design is settled.

Run with:  streamlit run draft_dash.py
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
    "Explore Data",
    "Useful Links",
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
        "TODO: one or two sentences on why this dashboard exists. "
        "Example: help students and employees see how people get to campus, "
        "find lower-carbon options that fit their trip, and share feedback."
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
        "2025-26 Commuter Report: share of commute trips made by driving alone."
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
        ("JackPass", "Unlimited bus rides, free for students and a small fee for faculty/staff."),
        ("Humboldt Bike Share", "Bikes available on campus and in the community for discounted rental."),
        ("Bicycle Learning Center", "Free bike maintenance and instruction."),
        ("Free Ride-match", "Connects drivers and riders for carpooling and long-distance trips."),
        ("ZipCar", "Cars on demand by the hour or day. ZipCar covers gas, insurance and parking."),
        ("Discounted express buses", "Redwood Express Bus to Sonoma County, plus Amtrak buses and trains."),
    ]
    for name, desc in options:
        with st.container(border=True):
            st.subheader(name)
            st.write(desc)
            st.caption("TODO: add link and how to get started")

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
    "Driving or motorcycling alone",
    "University shuttle",
    "Carpool or vanpool with others",
    "Riding the bus",
    "Bicycling, scooter, skateboard or other non-gas mode",
    "Uber or Lyft",
    "Other",
]
DRIVE_MODES = {"Driving or motorcycling alone", "Carpool or vanpool with others"}
BIKE_MODE = "Bicycling, scooter, skateboard or other non-gas mode"

WEEKS = {
    "Student": ["<16", "16", "32", "37", "40", "42", ">42"],
    "Faculty": ["<18", "18", "36", "41", "44", "46", ">46"],
    "Staff/Admin": ["<24", "24-26", "45-47", "42-44", "50-51"],
}
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
    "I knew about it, but wouldn't have used it",
    "I didn't know, but now I'll probably use it",
    "I knew about it but didn't use it",
    "I used it!",
]


def render_survey():
    st.title("Take the Survey")
    st.caption(
        "DRAFT: a short version of the annual commuter survey. "
        "Answers are not saved anywhere yet, they only show up in this session."
    )

    # --- Role (decides which Q4-6 version shows) ---------------------------
    role = st.radio(
        "I am a...", ["Student", "Faculty", "Staff/Admin"], index=None, horizontal=True
    )
    if role is None:
        st.info("Please select an answer above.")
        return

    # --- Q2 housing --------------------------------------------------------
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

    # --- Q3 days per week --------------------------------------------------
    days = st.select_slider(
        "How many days a week do you commute to the university "
        "(in person or by telecommuting)?",
        options=[1, 2, 3, 4, 5, 6, 7],
        value=5,
    )

    # --- Q4-6: role-specific weeks per year (branch on role) ----------------
    weeks = st.selectbox(
        f"[{role} only] Between the end of last May and the end of this May, "
        "about how many weeks will you have come to the university?",
        WEEKS[role],
        index=None,
    )

    # --- Q7 mode mix (must total 100%) --------------------------------------
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

    # --- Q8-Q10: follow-ups that only appear for certain answers ------------
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

    # --- Q11 backup mode and barrier ----------------------------------------
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

    # --- Q12 location -------------------------------------------------------
    st.subheader("Where you commute from")
    city = st.text_input("City")
    zip_code = st.text_input("Zip code")

    # --- Q13 resource awareness ---------------------------------------------
    st.subheader("Transportation resources")
    resource_answers = {}
    for r in RESOURCES:
        resource_answers[r] = st.selectbox(r, KNOWLEDGE, index=None, key=f"res_{r}")

    # --- Q14 comments ---------------------------------------------------------
    comment = st.text_area("What changes would make it easier to get to campus without a car?")

    # --- Submit ---------------------------------------------------------------
    if st.button("Submit", type="primary"):
        if chosen and total != 100:
            st.error("Please make your mode percentages total 100% before submitting.")
        else:
            st.session_state["last_response"] = {
                "role": role, "housing": housing, "days_per_week": days,
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


# ---------------------------------------------------------------------------
# USEFUL LINKS
# ---------------------------------------------------------------------------
def render_links():
    st.title("Useful Links")

    st.subheader("Commute data and reports")
    st.markdown(
        "- [Cal Poly Humboldt Transportation Dashboard (Morgan's commuter report)]"
        "(https://www.humboldt.edu/sustainable-campus/sustainability-dashboard/transportation)"
    )

    st.subheader("Getting around")
    st.markdown(
        "- TODO: transit schedules and maps\n"
        "- TODO: JackPass\n"
        "- TODO: Humboldt Bike Share\n"
        "- TODO: Bicycle Learning Center\n"
        "- TODO: Ride-match\n"
        "- TODO: ZipCar\n"
        "- TODO: Transportation & Parking Services"
    )

    st.subheader("Project")
    st.markdown("- TODO: course page, contact")


RENDERERS = {
    "Home": render_home,
    "Transportation Info": render_transportation,
    "Take the Survey": render_survey,
    "Explore Data": render_data,
    "Useful Links": render_links,
}
RENDERERS[section]()
