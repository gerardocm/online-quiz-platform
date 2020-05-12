let deleteQuestion;
let deleteMultichoiceQuestion;
let deleteVotingQuestion;

$(document).ready(function() {
  let questionSetId;
  let questionOptionCount;
  $("#question-set-error").hide();
  $("#question-set-success").hide();
  getQuestionSetId();
  changeBtnSubmitLabel();
  $("body").addClass("bkg-primary-light");

  function submitUpdateQuestionSet() {
    const url = "/create-question-set/" + questionSetId;
    let formData = $("#question-set-form").serializeArray();
    $.post(url, formData, (success) => {
      $("#question-set-success").show();
      setTimeout(() => {
        $("#question-set-success").hide();
      }, 2000);
    })
    .fail(() => {
        $("#question-set-error").hide();
    });
  }

  function getManualForm() {
    const url = "/create-question-set/" + questionSetId + "/manual-question";
    $.get(url, function(data, status) {
      if(status == "success") {
        $("#create-question-form").empty();
        $("#create-question-form").append(data);
        $("#alert-question-error").hide();
        $("#alert-question-success").hide();
        $("#manual-question-form").on('submit', (evt) => {
          evt.preventDefault();
          submitManualQuestion();
        });
      }
      else {
        console.error(err);
      }
    });
  };

  function submitManualQuestion() {
    const url = "/create-question-set/" + questionSetId + "/manual-question";
    let formData = $("#manual-question-form").serializeArray();
    $("#alert-question-error").hide();
    $.post(url, formData, (success) => {
      $("#alert-question-success").show();
      $("#manual-question-form").hide();
      setTimeout(() => {
        $("#alert-question-success").hide();
        $("#create-question-form").empty();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-question-error").show();
    });
  }

  function getMultichoiceForm() {
    const url = "/create-question-set/" + questionSetId + "/multichoice-question";
    $.get(url, function(data, status){
      if(status == "success") {
        $("#create-question-form").empty();
        $("#create-question-form").append(data);
        $("#alert-question-error").hide();
        $("#alert-question-success").hide();
        questionOptionCount = 1;
        $("#multichoice-question-form").on('submit', (evt) => {
          evt.preventDefault();
          submitMultichoiceQuestion();
        });
        $("#btn-delete-option").on("click", function() {
          deleteOption($(this).parent().parent());
        });
        $("#btn-add-option").on("click", function() {
          addOption("voting");
        });
        $("#checkbox-1").change(function() {
          clearCheckboxes($(this));
        });
      }
      else {
        console.error(err);
      }
    });
  };

  function submitMultichoiceQuestion() {
    const url = "/create-question-set/" + questionSetId + "/multichoice-question";
    let formData = $("#multichoice-question-form").serializeArray();
    formData.push(getFormOptions("multichoice"));
    $("#alert-question-error").hide();
    $.post(url, formData, (success) => {
      $("#alert-question-success").show();
      $("#multichoice-question-form").hide();
      setTimeout(() => {
        $("#alert-question-success").hide();
        $("#create-question-form").empty();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-question-error").show();
    });
  }

  function getVotingForm() {
    const url = "/create-question-set/" + questionSetId + "/voting-question";
    $.get(url, function(data, status){
      if(status == "success") {
        $("#create-question-form").empty();
        $("#create-question-form").append(data);
        $("#alert-question-error").hide();
        $("#alert-question-success").hide();
        questionOptionCount = 1;
        $("#voting-question-form").on('submit', (evt) => {
          evt.preventDefault();
          submitVotingQuestion();
        });
        $("#btn-delete-option").on("click", function() {
          deleteOption($(this).parent().parent());
        });
        $("#btn-add-option").on("click", function() {
          addOption("voting");
        });
      }
      else {
        console.error(err);
      }
    });
  };

  function submitVotingQuestion() {
    const url = "/create-question-set/" + questionSetId + "/voting-question";
    let formData = $("#voting-question-form").serializeArray();
    formData.push(getFormOptions("voting"));
    $("#alert-question-error").hide();
    $.post(url, formData, (success) => {
      $("#alert-question-success").show();
      $("#voting-question-form").hide();
      setTimeout(() => {
        $("#alert-question-success").hide();
        $("#create-question-form").empty();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-question-error").show();
    });
  }

  function getFormOptions(questionType) {
    let children = $("#answer-options").children();
    let options = {
      name: "options",
      value: []
    };
    children.each(function() {
      let input = $(this).find("#input-col").find("#option");
      if(questionType === "multichoice") {
        let checkbox = $(this).find(".form-check").find(".form-check-input");
        options.value.push(JSON.stringify({
          "option": input.val(),
          "is_correct": checkbox.is(':checked')
        }));
      }
      else if(questionType === "voting") {
        options.value.push(JSON.stringify({
          "option": input.val()
        }));
      }
    });
    console.log('options.value :>> ', options.value);
    options.value = "["+options.value.toString()+"]";
    return options;
  }

  function getQuestionSetId() {
    let path = window.location.pathname;
    pathArray = path.split("/");
    if(pathArray.length <= 0) 
      return;
    questionSetId = pathArray[pathArray.length-1];
    if(questionSetId)
      setClickEvt();
  }

  function addOption(questionType) {
    let childrenLen = $("#answer-options").children().length;
    if(childrenLen == 5)
      return;
    
    questionOptionCount++;
    let newOption = $("#answer-options > :first-child").first().clone();
    const newId = questionOptionCount;
    newOption.prop('id', newId);
    let input = newOption.find("#input-col").find("#option");
    input.val("");
    input.text("");
    newOption.appendTo("#answer-options");
    let deleteButton = newOption.find("#btn-delete-col").find("#btn-delete-option");
    deleteButton.on("click", function() {
      deleteOption($(this).parent().parent());
    });
    if(questionType === "multichoice") {
      let checkbox = newOption.find(".form-check").find(".form-check-input");
      checkbox.prop('id', "checkbox-"+newId);
      checkbox.prop('checked', false);
      checkbox.change(function() {
        clearCheckboxes($(this));
      });
    }
  }

  function deleteOption(option) {
    if($("#answer-options").children().length <= 1)
      return;
    option.remove();
  }

  function clearCheckboxes(checkbox) {
    let children = $("#answer-options").children();
    children.each(function() {
      let checkboxInput = $(this).find(".form-check").find(".form-check-input");
      if(checkbox.attr('id') != checkboxInput.attr('id'))
        checkboxInput.prop('checked', false);
    });
  }

  function changeBtnSubmitLabel() {
    if(!questionSetId)
      return;
      
    $("#question-set-submit > #submit").prop('value', 'Update');
    $("#question-set-form").on('submit', (evt) => {
      evt.preventDefault();
      submitUpdateQuestionSet();
    });
  }

  // function called directly in the html 
  deleteManualQuestion = function (questionId) {
    $.ajax({
      url: '/create-question-set/'+ questionSetId +'/manual-question/' + questionId,
      method: 'DELETE',
      contentType: 'application/json',
      success: function() {
        $("#manual-question-list > #" + questionId).remove();
      },
      error: function(request,msg,error) {
        console.error(error);
      }
   });
  }

  // function called directly in the html 
  deleteMultichoiceQuestion = function (questionId) {
    $.ajax({
      url: '/create-question-set/'+ questionSetId +'/multichoice-question/' + questionId,
      method: 'DELETE',
      contentType: 'application/json',
      success: function() {
        $("#multichoice-question-list > #" + questionId).remove();
      },
      error: function(request,msg,error) {
          // handle failure
          console.error(error);
      }
   });
  }

  // function called directly in the html 
  deleteVotingQuestion = function (questionId) {
    $.ajax({
      url: '/create-question-set/'+ questionSetId +'/voting-question/' + questionId,
      method: 'DELETE',
      contentType: 'application/json',
      success: function() {
        $("#voting-question-list > #" + questionId).remove();
      },
      error: function(request,msg,error) {
        console.error(error);
      }
   });
  }

  function setClickEvt() {
    $("#add-manual").on("click", () => {
      getManualForm();
    });
    $("#add-multichoice").on("click", () => {
      getMultichoiceForm();
    });
    $("#add-voting").on("click", () => {
      getVotingForm();
    });
  }
  
});