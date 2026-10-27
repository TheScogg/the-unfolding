// SPDX-License-Identifier: MIT
"use strict";

document.documentElement.classList.add("js");

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#site-nav");
menuButton.hidden = false;
function closeMenu() {
  navigation.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}
menuButton.addEventListener("click", () => {
  const expanded = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(expanded));
  navigation.classList.toggle("is-open", expanded);
});
navigation.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});

const tabList = document.querySelector(".belief-tabs");
const tabs = [...tabList.querySelectorAll('[role="tab"]')];
function selectBelief(index, moveFocus = false) {
  tabs.forEach((tab, i) => {
    const selected = i === index;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
    document.getElementById(tab.getAttribute("aria-controls")).hidden = !selected;
  });
  if (moveFocus) tabs[index].focus();
}
tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => selectBelief(i));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (i + 1) % tabs.length;
    if (event.key === "ArrowLeft") next = (i + tabs.length - 1) % tabs.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = tabs.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      selectBelief(next, true);
    }
  });
});
tabList.hidden = false;
selectBelief(0);

const exercise = document.getElementById("attention-exercise");
const toggle = document.getElementById("timer-toggle");
const reset = document.getElementById("timer-reset");
const display = document.getElementById("timer-display");
const progress = document.getElementById("timer-progress");
const status = document.getElementById("timer-status");
let remaining = 60;
let deadline = 0;
let interval = null;
function paintTimer() {
  const seconds = Math.max(0, Math.ceil(remaining));
  display.textContent = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  progress.style.strokeDashoffset = String(339.292 * remaining / 60);
}
function stopTicking() {
  if (interval !== null) window.clearInterval(interval);
  interval = null;
}
function tick() {
  remaining = Math.max(0, (deadline - performance.now()) / 1000);
  paintTimer();
  if (remaining === 0) {
    stopTicking();
    toggle.textContent = "Begin again";
    status.textContent = "The minute is yours. Carry a little of that attention with you.";
  }
}
toggle.addEventListener("click", () => {
  if (interval !== null) {
    tick();
    stopTicking();
    toggle.textContent = remaining > 0 ? "Continue" : "Begin again";
    status.textContent = "Paused. There is no hurry.";
    return;
  }
  if (remaining <= 0) remaining = 60;
  deadline = performance.now() + remaining * 1000;
  toggle.textContent = "Pause";
  status.textContent = "Notice one ordinary thing. Ask: what makes this possible?";
  reset.hidden = false;
  interval = window.setInterval(tick, 200);
  paintTimer();
});
reset.addEventListener("click", () => {
  stopTicking();
  remaining = 60;
  toggle.textContent = "Begin one minute";
  status.textContent = "You can pause or stop whenever you wish.";
  reset.hidden = true;
  paintTimer();
});
exercise.hidden = false;
paintTimer();
