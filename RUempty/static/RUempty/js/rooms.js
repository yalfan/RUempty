document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', (event) => {
      const element = event.target;
      if (element.className.includes('switch-open-occupied-button')) {
        displayOpenOrOccupied(element);
      }
      else if (element.className.includes('display-class-button')) {
        displayOccupiedClass(element);
      }
  });
  loadCourses();
});


function displayOpenOrOccupied(btn) {
  let roomNumber = btn.classList[1];
  let container = document.querySelector(`.room-${roomNumber}`);
  
  let switchButton = container.querySelector(".switch-open-occupied-button");
  if (switchButton.innerHTML.includes("Occupied")) {
    switchButton.innerHTML = "View Open Times";
  }
  else {
    switchButton.innerHTML = "View Occupied Times";
  }
  
  let openTimes = container.querySelectorAll(".open-time-item");
  openTimes.forEach(time => {
    if (time.style.display === "block") {
      time.style.display = "none";
    }
    else {
      time.style.display = "block";
    }
  });
  
  let occupiedTimes = container.querySelectorAll(".occupied-time-item");
  occupiedTimes.forEach(time => {
    if (time.style.display === "block") {
      time.style.display = "none";
    }
    else {
      time.style.display = "block";
    }
  });
  
}

function displayOccupiedClass(btn) {
  // console.log(btn.parentNode);
  let parent = btn.parentNode.parentNode;
  if (btn.style.backgroundImage === "url(\"/static/RUempty/images/dropdown.png\")") {
    btn.style.backgroundImage = "url(\"/static/RUempty/images/slideup.png\")";
  }
  else {
    btn.style.backgroundImage = "url(\"/static/RUempty/images/dropdown.png\")";
  }
  // console.log(parent.children);
  // console.log(parent.nextElementSibling);
  let course = parent.nextElementSibling;
  let children = course.children;
  if (course.style.height === "0px") {
    setTimeout(() => {
      for (let child of children) {
        child.style.display = "block";
      }
    }, 100);
    course.style.height = "100px";
  }
  else {
    setTimeout(() => {
      for (let child of children) {
        child.style.display = "none";
      }
    }, 100);
    course.style.height = "0px";
  }
}

function loadCourses() {
  // console.log(roomCourses);
  for (const property in roomCourses) {
    let roomNumber = property.split(",")[0];
    let startTime = property.split(",")[1].split(" -> ")[0]
    let endTime = property.split(",")[1].split(" -> ")[1]
    // console.log(roomCourses[property]);
    
    let room = document.querySelector(`.room-${roomNumber}`);
    let times = room.querySelectorAll('.occupied-time-time');
    times.forEach(time => {
      let sTime = time.textContent.split(" -> ")[0];
      let eTime = time.textContent.split(" -> ")[1];
      if (startTime === sTime && endTime === eTime) {
        let information = time.parentNode.parentNode.querySelector('.occupied-time-class');
        let className = information.querySelector('.class-name');
        let instructors = information.querySelector('.class-instructors');
        className.textContent = roomCourses[property][0];
        instructors.textContent = "Instructor(s): " + roomCourses[property][1].join(" & ");
      }
    })
  }
}

