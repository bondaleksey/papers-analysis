function are_cookies_enabled(){
    var cookieEnabled = (navigator.cookieEnabled) ? true : false;
    if (typeof navigator.cookieEnabled == "undefined" && !cookieEnabled){ 
        document.cookie="testcookie";
        cookieEnabled = (document.cookie.indexOf("testcookie") != -1) ? true : false;
    }
    return (cookieEnabled);
}
if (are_cookies_enabled==false) {
	alert("В Вашем браузере отключено хранение файлов cookies! Для работы на сайте eLIBRARY.RU они должны быть включены.");
}

var supportsSVG = !!document.createElementNS && !!document.createElementNS("http://www.w3.org/2000/svg", "svg").createSVGRect;
var didScroll = false;
var didScroll2 = false;
var ret = false;

function alerts(mess){
    $.fancybox('<table width=400 cellspacing=3 cellpadding=0 border=0><tr><td width=40 align=right valign=top><img src="/images/but_orange_!.gif" width=15 height=15 hspace=10 border=0></td><td width=351 align=left valign=top class="redref"><font color=#00008f>' + mess + '</font></td></tr></table><div style="width:67px; margin:10px auto;" class="butblue" onClick="$.fancybox.close()">Закрыть</div>', {
      title : '',
	  padding : 20,     
	  width : 440,
	  scrolling : 'no',
	  overlayOpacity : 0.3,	
	  overlayColor : '#000',
	  speedIn : 500,
	  hideOnOverlayClick : false,
	  enableEscapeButton : true
    });
}
function confirms(mess,callback) {
    $.fancybox('<table width=400 cellspacing=3 cellpadding=0 border=0><tr><td width=40 align=right valign=top><img src="images/but_orange_!.gif" width=15 height=15 hspace=10 border=0></td><td width=351 align=left valign=top class="redref"><font color=#00008f>' + mess + '</font></td></tr><tr><td colspan=2 align=center valign=top><div style="height:15px;">&nbsp;</div><table width=175 cellspacing=0 cellpadding=0 border=0><tr align=center class="menus"><td width=80><div class="butred" style="width: 67px;" onClick="ret=true;$.fancybox.close()">OK</div></td><td width=5></td><td width=90><div class="butblue" style="width: 77px;" onClick="ret=false;$.fancybox.close()">Отмена</div></td></tr></table><div style="height:5px;">&nbsp;</div></td></tr></table>', {
      title : '',
	  padding : 20,     
	  width : 440,
	  scrolling : 'no',
	  overlayOpacity : 0.3,	
	  overlayColor : '#000',
	  speedIn : 500,
	  hideOnOverlayClick : false,
	  enableEscapeButton : true,
      onClosed : function() {
        setTimeout(function(){ 
		  callback.call(this);
        }, 500); 
      }
    });
}

$(document).ready(function() { 

$('<div id="arrow">Вверх</div>').insertAfter('#footer');

function change_width(){
  var x = $(window).width();
  if (x<=1050) {
    $('#leftcol').width(170); 
	$('#rightcol').width(200); 
	$('#footer').width(970);
	$('#footer3').width(970);
	}
  else if (x>1234) {
    $('#leftcol').width(216); 
	$('#rightcol').width(246); 
	$('#footer').width(1062);
	$('#footer3').width(1062);
	}
  else {
    $('#leftcol').width(170+Math.floor((x-1050)/4)); 
	$('#rightcol').width(200+Math.floor((x-1050)/4));
	$('#footer').width(970+Math.floor((x-1050)/2));
	$('#footer3').width(970+Math.floor((x-1050)/2));
	}
}
$(window).resize(change_width);
change_width();

$(window).scroll(function() {
     didScroll = true;
    if ($(this).scrollTop() >= 400) {
        $('#arrow').fadeIn();
    }
        else {
       $('#arrow').fadeOut();
    };
 });

$('#arrow').click(function() {
    $('html, body').animate( {
        scrollTop: 0
    }, 'slow')
 })

setInterval(function() {
  if ( didScroll ) {
	didScroll=false;
	didScroll2=true;
    var panel=$('#panel')
    var paneld=$('#panel_default')
    var xd=$('#panel_default').offset().top;
    var xf=$('#footer').offset().top;
    var xp=panel.offset().top;
    var xw = $(window).height();
    var xt=$(window).scrollTop();
    var xz=panel.height();
	if (xt<xp-20 && xt<xd-20) {panel.animate({top: 0}, 400)}
    else if (xt>xp-20 && xt+20+xz>xf-20 && xw+xt>xf) {panel.animate({top: xf-xd-20-xz}, 400)}
    else if (xf<xp+xz+20 && xw+xt>xp+xz) {panel.animate({top: xf-xd-20-xz}, 400)}
    else if (xw+xt>xp+xz && xw<xz) {panel.animate({top: xw+xt-xd-xz-20}, 400)}
	else if (xt<xp-20 && xw<xz) {panel.animate({top: xt+20-xd}, 400)}
	else if (xw>xz) {panel.animate({top: xt+20-xd}, 400)}
    }
 }, 500);

});
$(function(){
   $('#fancybox-wrap').easydrag();
});
