document.addEventListener('DOMContentLoaded', () => {
  onPageLoad();
  if (document.querySelector("#update-db-button")) {
    document.querySelector("#update-db-button").addEventListener("click", () => {
      updateDB();
    });
  }
  
  document.querySelector("#id_campus").addEventListener("change", () => {
    updateBuildings();
    toggleBuildingSelect();
  });
  
  document.querySelector("#id_building").addEventListener("change", () => {
    toggleSubmitBtn();
  });
});

function onPageLoad() {
  let day;
  switch (new Date().getDay()) {
    case 0:
        day = "Monday";
        break;
    case 1:
        day = "Monday";
        break;
    case 2:
        day = "Tuesday";
        break;
    case 3:
        day = "Wednesday";
        break;
    case 4:
        day = "Thursday";
        break;
    case 5:
        day = "Friday";
        break;
    case 6:
        day = "Saturday";
        break;
  }
  document.querySelector("#id_day").value = day;
  
  document.querySelector("#id_campus").value = "Please choose a campus";
  
  document.querySelector("#id_building").disabled = true;
  
  document.querySelector("option[value='Please choose a campus']").setAttribute("disabled", 'disabled');
  document.querySelector("option[value='Please choose a campus first']").setAttribute("disabled", 'disabled');
}


function updateDB() {
  fetch("/update_db", {
    method: "POST",
    headers: {
      'X-CSRFToken': csrfToken, // Include the CSRF token in the headers
    },
  }).then((res) => {
    console.log(res);
  })
}

function toggleBuildingSelect() {
  const buildingSelect = document.querySelector("#id_building");
  if (buildingSelect.disabled)
    buildingSelect.disabled = !buildingSelect.disabled;
  let defaultBuildingSelect = document.querySelector("option[value='Please choose a campus first']");
  if (defaultBuildingSelect) {
    defaultBuildingSelect.value = "Please choose a building";
    defaultBuildingSelect.text = "Please choose a building";
  }
}

function updateBuildings() {
  let campus = document.querySelector("#id_campus").value;
  let buildingSelectForm = document.querySelector("#id_building");
  fetch(`/buildings/${campus}`, {
      method: "GET",
      headers: {
        'X-CSRFToken': csrfToken, // Include the CSRF token in the headers
      },
    })
    .then(res => res.json())
    .then(data => {
      buildingSelectForm.innerHTML = "";
      let buildings = data.buildings;
      buildingSelectForm.appendChild(new Option("Please choose a building", "Please choose a building"))
      for (let building in buildings) {
        let newBuilding = new Option(buildings[building], buildings[building]);
        buildingSelectForm.appendChild(newBuilding);
      }
    })
    .then(() => {
      let defaultBuildingSelect = document.querySelector("option[value='Please choose a building']");
      if (defaultBuildingSelect) {
        defaultBuildingSelect.disabled = true;
      }
    });
}

function toggleSubmitBtn() {
  let submitBtn = document.querySelector("#submitBtn");
  if (submitBtn.disabled)
    submitBtn.disabled = false;
  // let roomForm = document.querySelector("form[name='myForm']");
  // let campus = document.querySelector("#id_campus").value;
  // let building = document.querySelector("#id_building").value;
  // roomForm.action = `rooms/${campus}/${building}`;
}