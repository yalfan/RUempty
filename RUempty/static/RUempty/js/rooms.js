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
  let parent = btn.parentNode;
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
  let rooms = document.querySelectorAll('.room-card');
  console.log(roomCourses);
  for (let course of roomCourses) {
    console.log(course);
  }
  // rooms.forEach(room => {
  //   let roomNumber = room.classList[room.classList.length-1].split("-")[1];
  //   let times = room.querySelectorAll('.occupied-time-time');
  //   console.log(times);
  //   times.forEach(time => {
  //     console.log(`Room: ${roomNumber}, Occupied at: ${time.textContent}`)
  //   })
  // })
}

