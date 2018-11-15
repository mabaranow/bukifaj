$(function () {

  $(".js-create-book").click(function () {
    var form = $(this);
    console.log(form)
    $.ajax({
      url: 'add_book',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

});