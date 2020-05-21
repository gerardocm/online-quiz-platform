$(document).ready(function() {
  $(".alert").hide();
  $("#answer-note").show();
  $("#empty-note").show();

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

  submitAnsMultiQuestion = function(questionSetId, questionId) {
    const ans = $("input[name=multichoice-answer-question-"+questionId+"]:checked").prop('id');
    const ansData = {
      answer: ans
    };

    if(!ansData.answer) {
      $("#alert-error-multichoice-"+questionId).show();
      setTimeout(() => {
        $("#alert-error-multichoice-"+questionId).hide();
      }, 2000);
      return;
    }

    const url ='/question-set/'+questionSetId+'/multichoice-question/'+questionId+'/answer/';
    $.post(url, ansData, (success) => {
      $("#alert-success-multichoice-"+questionId).show();
      setTimeout(() => {
        $("#alert-success-multichoice-"+questionId).hide();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-error-multichoice-"+questionId).show();
    });
  }

  submitAnsVotingQuestion = function(questionSetId, questionId) {
    const ans = $("input[name=voting-answer-question-"+questionId+"]:checked").prop('id');
    const ansData = {
      answer: ans
    };
    console.log('ans :>> ', ans);
    if(!ansData.answer) {
      $("#alert-error-voting-"+questionId).show();
      setTimeout(() => {
        $("#alert-error-voting-"+questionId).hide();
      }, 2000);
      return;
    }

    const url ='/question-set/'+questionSetId+'/voting-question/'+questionId+'/answer/';
    $.post(url, ansData, (success) => {
      $("#alert-success-voting-"+questionId).show();
      setTimeout(() => {
        $("#alert-success-voting-"+questionId).hide();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-error-voting-"+questionId).show();
    });
  }
});