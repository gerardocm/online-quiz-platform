$(document).ready(function() {
  let questionSetId;
  let questionOptionCount;
  getQuestionSetId();
  changeBtnSubmitLabel();

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
          deleteMultichoiceOption($(this).parent().parent());
        });
        $("#btn-add-option").on("click", function() {
          addMultichoiceOption();
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
    formData.push(getFormOptions());
    $("#alert-question-error").hide();
    $.post(url, formData, (success) => {
      $("#alert-question-success").show();
      $("#multichoice-question-form").hide();
      setTimeout(() => {
        $("#alert-question-success").hide();
        $("#create-question-form").empty();
      }, 2000);
    })
    .fail(() => {
      $("#alert-question-error").show();
    });
  }

  function getFormOptions() {
    let children = $("#answer-options").children();
    let options = {
      name: "options",
      value: []
    };
    children.each(function() {
      let input = $(this).find("#input-col").find("#option");
      let checkbox = $(this).find(".form-check").find(".form-check-input");
      options.value.push(JSON.stringify({
        "option": input.val(),
        "is_correct": checkbox.is(':checked')
      }));
    });
    options.value = "["+options.value.toString()+"]";
    return options;
  }
  
  function getVotingForm() {
    const url = "/create-question-set/" + questionSetId + "/voting-question";
    $.get(url, function(data, status){
      if(status == "success") {
        $("#create-question-form").empty();
        $("#create-question-form").append(data);
      }
      else {
        console.error(err);
        // alert-question-error
      }
    });
  };

  function getQuestionSetId() {
    let path = window.location.pathname;
    pathArray = path.split("/");
    if(pathArray.length <= 0) 
      return;
    questionSetId = pathArray[pathArray.length-1];
    if(questionSetId)
      setClickEvt();
  }

  function addMultichoiceOption() {
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
      deleteMultichoiceOption($(this).parent().parent());
    });
    let checkbox = newOption.find(".form-check").find(".form-check-input");
    checkbox.prop('id', "checkbox-"+newId);
    checkbox.prop('checked', false);
    checkbox.change(function() {
      clearCheckboxes($(this));
    });
  }

  function deleteMultichoiceOption(option) {
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
    if(questionSetId)
      $("#question-set-submit > #submit").prop('value', 'Update');
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