var wrapper = document.getElementById("signature-pad");
var clearButton = wrapper.querySelector("[data-action=clear]");
var undoButton = wrapper.querySelector("[data-action=undo]");
var recogButton = wrapper.querySelector("[data-action=recog]");
var result = wrapper.querySelector("#result");
var canvas = wrapper.querySelector("canvas");

var signaturePad = new SignaturePad(canvas, {
  // It's Necessary to use an opaque color when saving image as JPEG;
  // this option can be omitted if only saving as PNG or SVG
  backgroundColor: 'rgb(255, 255, 255)',
  minWidth: 4,
  maxWidth: 6
});

// Adjust canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
// This also causes canvas to be cleared.
function resizeCanvas() {
  // When zoomed out to less than 100%, for some very strange reason,
  // some browsers report devicePixelRatio as less than 1
  // and only part of the canvas is cleared then.
  var ratio = Math.max(window.devicePixelRatio || 1, 1);
  var data = signaturePad.toDataURL();
  // This part causes the canvas to be cleared
  canvas.width = canvas.offsetWidth * ratio;
  canvas.height = canvas.offsetHeight * ratio;
  canvas.getContext("2d").scale(ratio, ratio);

  // This library does not listen for canvas changes, so after the canvas is automatically
  // cleared by the browser, SignaturePad#isEmpty might still return false, even though the
  // canvas looks empty, because the internal data of this library wasn't cleared. To make sure
  // that the state of this library is consistent with visual state of the canvas, you
  // have to clear it manually.
  signaturePad.clear();
  signaturePad.fromDataURL(data);
}

// On mobile devices it might make more sense to listen to orientation change,
// rather than window resize events.
window.onresize = resizeCanvas;
resizeCanvas();

clearButton.addEventListener("click", function (event) {
  signaturePad.clear();
});

undoButton.addEventListener("click", function (event) {
  var data = signaturePad.toData();
  if (data) {
    data.pop(); // remove the last dot or line
    signaturePad.fromData(data);
  }
});

recogButton.addEventListener("click", function () {
  var data = signaturePad.toDataURL();

  var req = new XMLHttpRequest();
  req.onreadystatechange = function () {
    if (req.readyState == req.DONE) {
      var obj = JSON.parse(req.responseText);
      result.textContent = obj.letter;
      if (obj.letter == '-') {
        alert("Could not identify your letter!");
      }
    }
  };
  req.onerror = function () {
    alert("Error occured. Please try again later");
  };
  req.open("POST", "/upload", true);
  req.send(data);
});