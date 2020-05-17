let addUser;
let displayUserForm;
let hideUserForm;
let removeUser;
let markUser;

$(document).ready(function() {
  let questionSetId;
  getQuestionSetId();
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
    console.log('val :>> ', val);
    let url = '/users?email=' + val;
    $.get(url, function(data, status) {
      if(status == "success") {
        let users = data.users;
        console.log('data :>> ', data);
        console.log('data :>> ', data.users);
        $("#user-search-list").empty();
        if(!data.users) {
          console.log('empty :>> ');
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
    console.log('adduserId :>> ', userId);
    let data = {
      "user": userId, 
      "question_set": questionSetId, 
    };
    console.log('data :>> ', data);
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
    let redirectPath = "/mark-user-question-set/" + questionSetId;
    redirectPath += "/user/" + userId;
    window.location.href = redirectPath;
  }
});