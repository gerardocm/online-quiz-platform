$(document).ready(function() {
  getQuestionSetId();
  setQuestionSetDate();
  setQuestionSetPrivacy();

  function getQuestionSetId() {
    let path = window.location.pathname;
    pathArray = path.split("/");

    if(pathArray.length <= 2) 
      return;

    questionSetId = pathArray[pathArray.length-1];
  }

  function setQuestionSetPrivacy() {
    console.log('here :>> ');
    if($('#public').length) {
      $("#privacy-title").text("PUBLIC");
      $("#privacy-text").text("All registered users have access");
    }
    else if($('#private').length) {
      $("#privacy-title").text("PRIVATE");
      $("#privacy-text").text("Only invited users have access");
    }
  }

  function setQuestionSetDate() {
    let rawDate = $('#date-created').text();
    let date = new Date(rawDate);
    $('#date-created').text("Date created: " + date.toDateString());
  }
});