$(function () {
    $("#activador").click(function (e) {
      e.preventDefault();
      $('body').toggleClass('letshidesome');
      $('#email-preview').toggleClass('emailpreview');
      $('#sidenav').toggleClass('side_nav');
    });
  
});