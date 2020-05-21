let submitMark;
let editMark;
let cancelEditMark;

$(document).ready(function() {
  $("#alert-success").hide();
  $("#alert-error").hide();
  $("body").addClass("bkg-primary-light");
  hideMarkingForm();

  function hideMarkingForm() {
    const questions = $('#manual-questions').children();
    questions.each(function() {
      let inputGroup = $(this).find(".input-group");
      inputGroup.hide();
    });
  }

  editMark = function(questionId) {
    const questions = $('#manual-questions').children();
    questions.each(function() {
      let input = $(this).find("#input-group-mark-"+questionId);
      let markLabel = $(this).find("#answer-mark-"+questionId);
      input.show();
      markLabel.hide();
      if(input.val() == "None")
        input.val('');
    });
  }

  submitMark = function(questionId, questionAnsId) {
    let markData = {
      mark: $('#input-mark-' + questionId).val()
    };
    const url ='/manual-question/answer/' + questionAnsId;
    $.post(url, markData, (success) => {
      $("#alert-success").show();
      setTimeout(() => {
        $("#alert-success").hide();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-error").show();
    });
  }

  cancelEditMark = function(questionId) {
    const questions = $('#manual-questions').children();
    questions.each(function() {
      let input = $(this).find("#input-group-mark-"+questionId);
      let markLabel = $(this).find("#answer-mark-"+questionId);
      input.hide();
      markLabel.show();
    });
  }
  
});