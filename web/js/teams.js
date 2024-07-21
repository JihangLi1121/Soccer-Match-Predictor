async function main() {
    let res = await fetch("data/teams.json");
    const TEAMS = await res.json();

    const statModal = new bootstrap.Modal(document.getElementById("statModal"), {
        keyboard: true, backdrop: true
    });

    const findTeamByName = (name) => {
        for (let team of TEAMS.teams) {
            if (team.name === name) {
                return team;
            }
        }
    }

    let tc = 0;
    for (let team of TEAMS.teams) {
        let card = document.createElement("div");
        card.insertAdjacentHTML("beforeend", `<div class="row">
                <div class="col-sm-4">
                    <img alt="${team.name}" src="${team.logo}" class="logo-img" />
                </div>
                <div class="col-sm-6 d-flex flex-column justify-content-center">
                    <h5>${team.name}</h5>
                </div>
            </div>`);
        card.className = "card mb-3 team-card";
        document.getElementById(`col${Math.floor(tc / 6)}`).appendChild(card);

        card.onclick = () => {
            document.getElementById("predictionRow").classList.add("d-none");
            document.getElementById("statModalTitle").innerText = team.name;
            document.getElementById("upcomingMatches").innerHTML = "";
            for (let match of TEAMS.matches) {
                if (match["Home Team"] === team.name || match["Away Team"] === team.name) {
                    let home = findTeamByName(match["Home Team"]);
                    let away = findTeamByName(match["Away Team"]);
                    let matchCard = document.createElement("div");
                    matchCard.insertAdjacentHTML("beforeend", `
                    <div class="card-body">
                        <div class="mb-0 w-100 text-center">
                            <h3 class="float-start mb-0">${home.id}</h3>
                            <h3 class="float-end mb-0">${away.id}</h3>
                        </div>
                        <br>
                        <br>
                        <span class="mb-0 w-100">
                            <span class="float-start">${match.Date}</span>
                            <span class="float-end">Matchday ${match.Matchday}</span>
                        </span>
                    </div>`)
                    matchCard.className = "card mb-3 match-card";
                    document.getElementById("upcomingMatches").appendChild(matchCard);
                    matchCard.onclick = async() => {
                        document.getElementById("SR_Matchday").innerText = match.Matchday;
                        let res = await fetch(`data/predicted_teams_classify/predicted_${team.id}.json`);
                        let stats = await res.json();
                        let homeWin = stats["Home Win Probability"][match.Matchday - 1] * 100;
                        let draw = stats["Draw Probability"][match.Matchday - 1] * 100;
                        let awayWin = stats["Away Win Probability"][match.Matchday - 1] * 100;
                        document.getElementById("SR_Name").innerText = `${home.id} vs ${away.id}`;
                        document.getElementById("winChance").style.width = `${homeWin}%`;
                        document.getElementById("winChance").innerText = `${Math.round(homeWin)}% ${home.id}`;
                        document.getElementById("loseChance").style.width = `${awayWin}%`;
                        document.getElementById("loseChance").innerText = `${Math.round(awayWin)}% ${away.id}`
                        document.getElementById("drawChance").style.width = `${draw}%`;
                        document.getElementById("drawChance").innerText = `${Math.round(draw)}% Draw`
                        document.getElementById("predictionRow").classList.remove("d-none");

                    }
                }
            }
            statModal.show()
        }
        tc += 1;
    }
}

main().then();
