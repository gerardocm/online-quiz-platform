// let submitMark;
// let editMark;
// let cancelEditMark;

$(document).ready(function() {
  $(".alert").hide();
  $("#answer-note").show();
  $("#empty-note").show();
  console.log('$("#alert-error") :>> ', $("#alert-error"));
//   $("body").addClass("bkg-primary-light");
//   hideMarkingForm();

//   function hideMarkingForm() {
//     const questions = $('#manual-questions').children();
//     questions.each(function() {
//       let inputGroup = $(this).find(".input-group");
//       inputGroup.hide();
//     });
//   }

//   editMark = function(questionId) {
//     const questions = $('#manual-questions').children();
//     questions.each(function() {
//       let input = $(this).find("#input-group-mark-"+questionId);
//       let markLabel = $(this).find("#answer-mark-"+questionId);
//       input.show();
//       markLabel.hide();
//       if(input.val() == "None")
//         input.val('');
//     });
//   }

  submitAnsManualQuestion = function(questionSetId, questionId) {
    let ansData = {
      answer: $.trim($('#answer-' + questionId).val())
    };
    if(!ansData.answer) {
      $("#alert-error-manual-"+questionId).show();
      setTimeout(() => {
        $("#alert-error-manual-"+questionId).hide();
      }, 2000);
      return;
    }
    const url ='/question-set/'+questionSetId+'/manual-question/'+questionId+'/answer/';
    $.post(url, ansData, (success) => {
      $("#alert-success-manual-"+questionId).show();
      setTimeout(() => {
        $("#alert-success-manual-"+questionId).hide();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-error-manual-"+questionId).show();
    });
  }

//   cancelEditMark = function(questionId) {
//     const questions = $('#manual-questions').children();
//     questions.each(function() {
//       let input = $(this).find("#input-group-mark-"+questionId);
//       let markLabel = $(this).find("#answer-mark-"+questionId);
//       input.hide();
//       markLabel.show();
//     });
//   }
  
});