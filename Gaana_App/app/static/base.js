var array=[];
var indx=-1;

$(document).ready(function() { 
  $('#audio-player').on('play',function(e){
    $('.mejs-time-rail').css("width","");
    $('.mejs-time-total').css("width","");
    });
    // $('#block_content').load('index');
    $bar = $('#block_content');
    console.log("in base js")
   $('a.anchor').click(function(e){
    e.preventDefault();
    // $('#block_content').load(url);
    //added by priya
        var targetUrl = $(this).attr('href'),
        targetTitle = $(this).attr('title');
        console.log("target URL"+targetUrl)
        window.history.pushState({url: "" + targetUrl + ""}, targetTitle, targetUrl);
        setCurrentPage(targetUrl);
    //added by priya ends
    var url=$(this).attr('href');
    var nav_html=$('#navbar').html();
    // localStorage.setItem('display', url);
    // localStorage.setItem('nav', nav_html);
    // console.log(localStorage.getItem('display'))

  });

    $('#signout').click(function(){
      document.getElementById("login").style.display="block"
        document.getElementById("signup").style.display="block"
        document.getElementById("signout").style.display="none"

    });
    $("#login-nav").click(function(event) {
     
          event.preventDefault();
          var form = $('#form1')[0];
          var data = new FormData(form);
          var url=$(form).attr('action');
          // url='/loginNext'
          alert(url)
          $.ajax({
            type: "POST",
             enctype: 'multipart/form-data',
             url:url,
             data: data,
              processData: false,
              contentType: false,
              cache: false,
              success: function (result) {
                      $('#block_content').html(result);
                      var nav_html=$('#navbar').html();

                      $('#navbar').html(nav_html)
                      console.log(nav_html)
                      // localStorage.setItem('display', $bar.html());
                      document.getElementById("login").style.display="none";
                      document.getElementById("signup").style.display="none";
                      document.getElementById("signout").style.display="block";
                      $('#login-modal').modal('hide');
                      // $('body').removeClass('modal-open');
              // $('div.modal-backdrop').remove();
                      },
                      error: function (event) {
                      console.log("ERROR : ", event);
            }
          });
    });
    $("#form2").submit(function(event) {
          event.preventDefault();
          var form = $('#form2')[0];
          var data = new FormData(form);
          var url=$(this).attr('action');
          $.ajax({
            type: "POST",
             enctype: 'multipart/form-data',
             url:url,
             data: data,
              processData: false,
              contentType: false,
              cache: false,
              success: function (result) {
                      $('#block_content').html(result);
                      console.log(result)
                      // localStorage.setItem('display', $bar.html());
                      document.getElementById("login").style.display="none";
                      document.getElementById("signup").style.display="none";
                      document.getElementById("signout").style.display="block";
                      $('#register-modal').modal('hide');
                      },
                      error: function (event) {
                      console.log("ERROR : ", event);
            }
          });
    });
     $("#search_form").submit(function(event) {
          event.preventDefault();
          var form = $('#search_form')[0];
          var data = new FormData(form);
          $.ajax({
            type: "POST",
             enctype: 'multipart/form-data',
             url:'/search',
             data: data,
              processData: false,
              contentType: false,
              cache: false,
              success: function (result) {
                      $('#block_content').html(result);
                      // localStorage.setItem('display', $bar.html());
                      // document.title = oPageInfo.title
                      // window.history.pushState(oPageInfo, oPageInfo.title, oPageInfo.url);

                      },
                      error: function (event) {
                      console.log("ERROR : ", event);
                      // window.history.pushState("Details", "Title", "/search");
            }
          });
    });

 
    // var block = localStorage.getItem('display');
    // var nav = localStorage.getItem('nav');
    // if (block !== null) {
      // $bar.html(block).show()
    // $bar.load(block);
      // $('#navbar').html('');
      // $('#navbar').html(nav);
      // console.log(nav);
      // console.log(block);
    // }
    // else{
      $bar.load('home')
    // }
    $('ul li').click(function(e){
        $('ul li').removeClass('active');
        $(this).addClass('active');

    });



$('#next').click(function(e){
      console.log("in next")
      indx=(indx+1)%array.length;
      path=array[indx][2];
      name=array[indx][0];
      img=array[indx][1];
      $('#audio-player').attr("src",path);
      $('#audio-player').attr("preload",'true');
      $('#audio-player').attr("autoplay",'true');
      $('#song-name-preview').text(name);
      $('.cover').attr('src',img);
      $('.cover').attr('width','110');
      $('.cover').attr('height','114');
      // $('.mejs-horizontal-volume-current').css('width','80px');
      // $('.mejs-horizontal-volume-handle').css('left','74px');
    });

    $('#prev').click(function(e){
      indx=(indx-1);
      if(indx<0)indx=array.length-1;
      path=array[indx][2];
      name=array[indx][0];
      img=array[indx][1];
     
      $('#audio-player').attr("src",path);
 $('#audio-player').attr("preload",'true');
 $('#audio-player').attr("autoplay",'true');
 $('#song-name-preview').text(name);
 $('.cover').attr('src',img);
 $('.cover').attr('width','110');
 $('.cover').attr('height','114');
//  $('.mejs-horizontal-volume-current').css('width','80px');
//  $('.mejs-horizontal-volume-handle').css('left','74px');
    });
// added by priya
$('#audio-player').on("ended",function(){
  indx=(indx+1)
  var audio=document.getElementById("audio-player")
  if(indx<array.length){
 
  path=array[indx][2]
  name=array[indx][0]
  img=array[indx][1]
  // $('#bottom-nav').css("display","block");
$('#audio-player').attr("src",path);
$('#audio-player').attr("preload",'true');

$("#audio-player").on("canplay",function(){
  if(indx==array.length){
    audio.pause()
  }
  else{
  audio.play()
  }
});
$('#song-name-preview').text(name);
$('.cover').attr('src',img);
$('.cover').attr('width','110');
$('.cover').attr('height','114');
  }

});

});


// added by priya
    // and load the url content
var setCurrentPage = function(url) {
  $('#block_content').load(url);
};

// added by priya
window.onpopstate = function(e) {
    setCurrentPage(e.state ? e.state.url : null);
};

