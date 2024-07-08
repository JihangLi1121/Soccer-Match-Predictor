const TEAMS = [{
    name: "FC Bayern München", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000G.svg"
}, {
    name: "Borussia Dortmund", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000007.svg"
}, {
    name: "RB Leipzig", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000017.svg"
}, {
    name: "1. FC Union Berlin", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000V.svg"
}, {
    name: "SC Freiburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000A.svg"
}, {
    name: "Bayer 04 Leverkusen", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000B.svg"
}, {
    name: "Eintracht Frankfurt", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000F.svg"
}, {
    name: "Vfl Wolfsburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000003.svg"
}, {
    name: "1. FSV Mainz 05", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000006.svg"
}, {
    name: "Borussia M'gladbach", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000004.svg"
}, {
    name: "Holstein Kiel", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000N5P.svg"
}, {
    name: "TSG Hoffenheim", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000002.svg"
}, {
    name: "SV Werder Bremen", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000E.svg"
}, {
    name: "Vfl Bochum 1848", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000S.svg"
}, {
    name: "FC Augsburg", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000010.svg"
}, {
    name: "VfB Stuttgart", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000D.svg"
}, {
    name: "FC St. Pauli", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000H.svg"
}, {
    name: "1. FC Heidenheim 1846", logo: "https://www.bundesliga.com/assets/clublogo/DFL-CLU-000018.svg"
}]

let tc = 0;
for (let team of TEAMS) {
    document.getElementById(`col${Math.floor(tc / 6)}`).insertAdjacentHTML("beforeend", `
        <div class="card mb-3 team-card">
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
