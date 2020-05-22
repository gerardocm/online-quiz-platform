$(document).ready(function() {
  let enumFilters = {
    isPublic: {
      filterVal:"ispublic",
      id:"is-public"
    },
    assigned: {
      filterVal:"assigned",
      id:"assigned"
    },
    owner: {
      filterVal:"owner",
      id:"owner"
    },
    submitted: {
      filterVal:"submitted",
      id:"submitted"
    }
  };
  setFilters();
  $('[data-toggle="tooltip"]').tooltip();

  function setFilters() {
    let filterUrl = window.location.search;
    if(!filterUrl) {
      $("#" + enumFilters.isPublic.id).prop('checked', true);
      $("#" + enumFilters.assigned.id).prop('checked', true);
      $("#" + enumFilters.owner.id).prop('checked', true);
      $("#" + enumFilters.submitted.id).prop('checked', true);
    }
    else {
      queryParams = filterUrl.split("=")[1];
      values = queryParams.split(",");

      if(values.includes(enumFilters.isPublic.filterVal))
        $("#" + enumFilters.isPublic.id).prop('checked', true);
      if(values.includes(enumFilters.assigned.filterVal))
        $("#" + enumFilters.assigned.id).prop('checked', true);
      if(values.includes(enumFilters.owner.filterVal)) {
        $("#" + enumFilters.owner.id).prop('checked', true);
        if(values.includes(enumFilters.submitted.filterVal))
          $("#" + enumFilters.submitted.id).prop('checked', true);
      }
    }
  }

  applyFilter = function(){
    let isPublic = $("#" + enumFilters.isPublic.id).is(':checked');
    let assigned = $("#" + enumFilters.assigned.id).is(':checked');
    let owner = $("#" + enumFilters.owner.id).is(':checked');
    let submitted = $("#" + enumFilters.submitted.id).is(':checked');

    let url = (isPublic || assigned || owner) ? '/quizzes?filter=' : '/quizzes';
    if(isPublic)
      url += enumFilters.isPublic.filterVal + ",";
    if(assigned)
      url += enumFilters.assigned.filterVal + ",";
    if(owner) {
      url += enumFilters.owner.filterVal + ",";
      if(submitted)
        url += enumFilters.submitted.filterVal;
    }

    window.location.href = url;
  }

  joinQuiz = function(userId,quizId) {
    console.log('userId :>> ', userId);
    console.log('quizId :>> ', quizId);
  }

});