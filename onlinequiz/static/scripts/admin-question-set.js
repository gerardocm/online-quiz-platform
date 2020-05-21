let addUser;
let displayUserForm;
let hideUserForm;
let removeUser;
let markUser;

$(document).ready(function() {
  let questionSetId;
  getQuestionSetId();
  setQuestionSetDate();
  setQuestionSetPrivacy();
  $("body").addClass("bkg-primary-light");
  $("#alert-error").hide();
  $("#alert-success").hide();
  $("#add-user").hide();
  $('[data-toggle="tooltip"]').tooltip();

  function getQuestionSetId() {
    let path = window.location.pathname;
    pathArray = path.split("/");

    if(pathArray.length <= 2) 
      return;

    questionSetId = pathArray[pathArray.length-1];
  }

  function setQuestionSetPrivacy() {
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

  displayUserForm = function() {
    $("#user-list-section").hide();
    $("#add-user").show();
  }

  hideUserForm = function() {
    $("#user-search-list").empty();
    $("#input-search-user").val('');
    $("#add-user").hide();
    $("#user-list-section").show();
  }

  searchUser = function() {
    let val = $("#input-search-user").val();
    let url = '/users?email=' + val;
    $.get(url, function(data, status) {
      if(status == "success") {
        $("#user-search-list").empty();
        if(!data.users) {
          $("#user-search-list").append(`
            <li class="list-group-item list-group-item-action list-group-item-light"
              id="li-user">
              No users found
            </li>
          `);
        }
        else {
          data.users.forEach( user => {
            $("#user-search-list").append(`
            <li class="list-group-item list-group-item-action list-group-item-light"
            id="li-user">
              <div class="row" >
                <div class="col-sm-11">
                ` + user.full_name + `
                </div>
                <div class="col-sm-1">
                  <button type="button" class="btn btn-outline-success" id="btn-add-user"
                    onclick="addUser(` + user.id + `)">
                    <i class="fas fa-plus-circle"></i>
                  </button>
                </div>
              </div>
            </li>
            `);
          });
        }
      }
      else {
        console.error(err);
      }
    });
  };

  addUser = function(userId) {
    let data = {
      "user": userId, 
      "question_set": questionSetId, 
    };
    const url = '/question-set-user';
    $.post(url, data, (success) => {
      $("#alert-success").show();
      setTimeout(() => {
        $("#alert-question-success").hide();
        $("#hideUserForm").empty();
        location.reload();
      }, 2000);
    })
    .fail(() => {
      $("#alert-error").show();
    });
  }

  removeUser = function(userId) {
    const url = '/question-set-user/user/' + userId;
    $.ajax({
      url: url,
      method: 'DELETE',
      contentType: 'application/json',
      success: function() {
        location.reload();
      },
      error: function(request,msg,error) {
        console.error(error);
      }
    });
  };

  markUser = function(userId) {
    let redirectPath = "/mark-question-set/" + questionSetId;
    redirectPath += "/user/" + userId;
    window.location.href = redirectPath;
  }

  deleteQuestionSet = function() {
    const url = '/question-set/' + questionSetId;
    $.ajax({
      url: url,
      method: 'DELETE',
      contentType: 'application/json',
      success: function() {
        window.location.href = '/';
      },
      error: function(request,msg,error) {
      }
    });
    $('#delete-quiz-modal').modal('hide');
  }
});