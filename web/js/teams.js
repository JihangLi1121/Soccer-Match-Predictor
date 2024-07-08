const TEAMS = [{
    name: "FC Bayern München",
    logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000G.svg",
    id: "Bayern Munich"
}, {
    name: "Borussia Dortmund", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000007.svg",
    id: "Dortmund"
}, {
    name: "RB Leipzig", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000017.svg",
    id: "RB Leipzig"
}, {
    name: "FC Union Berlin", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000V.svg",
    id: "Union Berlin"
}, {
    name: "SC Freiburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000A.svg",
    id: "Freiburg"
}, {
    name: "Bayer 04 Leverkusen", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000B.svg",
    id: "Bayer Leverkusen"
}, {
    name: "Eintracht Frankfurt", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000F.svg",
    id: "Eintracht Frankfurt"
}, {
    name: "Vfl Wolfsburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000003.svg",
    id: "Wolfsburg"
}, {
    name: "FSV Mainz 05", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000006.svg",
    id: "Mainz 05"
}, {
    name: "Borussia M'gladbach", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000004.svg",
    id: "Mönchengladbach"
}, {
    name: "Holstein Kiel", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000N5P.svg",
    id: "Kiel"
}, {
    name: "TSG Hoffenheim", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000002.svg",
    id: "Hoffenheim"
}, {
    name: "SV Werder Bremen", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000E.svg",
    id: "Werder Bremen"
}, {
    name: "Vfl Bochum 1848", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000S.svg",
    id: "Bochum"
}, {
    name: "FC Augsburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000010.svg",
    id: "Augsburg"
}, {
    name: "VfB Stuttgart", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000D.svg",
    id: "Stuttgart"
}, {
    name: "FC St. Pauli", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000H.svg",
    id: "Pauli"
}, {
    name: "FC Heidenheim 1846", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000018.svg",
    id: "Heidenheim"
}]

const statModal = new bootstrap.Modal(document.getElementById("statModal"), {
    keyboard: true,
    backdrop: true
});

statModal.show();

let tc = 0;
for (let team of TEAMS) {
    document.getElementById(`col${Math.floor(tc / 6)}`).insertAdjacentHTML("beforeend", `
        <div class="card mb-3 team-card" onclick="statModal.show()">
            <div class="row">
                <div class="col-sm-4">
                    <img src="${team.logo}" class="logo-img" />
                </div>
                <div class="col-sm-6 d-flex flex-column justify-content-center">
                    <h5>${team.name}</h5>
                </div>
            </div>
        </div>
    `)
    tc += 1;
}
