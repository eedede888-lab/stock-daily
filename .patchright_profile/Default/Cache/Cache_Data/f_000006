/*
http://patorjk.com/software/taag/#p=display&f=Small&t=width

   __                    
  / _|_ _ __ _ _ __  ___ 
 |  _| '_/ _` | '  \/ -_)
 |_| |_| \__,_|_|_|_\___|
                         
*/



function _checkapp() {
    var useragent = navigator.userAgent;
    var regex = new RegExp(/(WebView|(iPhone|iPod|iPad)(?!.*Safari\/)|Android.*(wv|.0.0.0))/gi);
    var str = Boolean(useragent.match(regex));
    return str;
}
function _s_get(name) { if(_checkapp()) { return $.session.get(name); } else { return localStorage.getItem(name); } }
function _s_set(name, input) { var date = new Date(), minutes = 30;
    date.setTime(date.getTime() + (minutes * 24 * 60 * 1000));
    if(_checkapp()) { return $.session.set(name, input); } else { return localStorage.setItem(name, input); }
}
function _s_clear() { if(_checkapp()) { $.session.clear(); } else { localStorage.clear(); }}
function _get_json(func, url, input1, input2) {
    $.ajax({
        url:            url,
        type:           'GET',
        dataType:       'json', 
        data: {},
        error: function(xhr) {},
        success: function(response) {},
        complete: function(response) {
            var data = JSON.parse(response.responseText);
            //console.log('complete: ', data);
            func(data, input1, input2);
        }
    });
}













/*

       _     _          _ 
  __ _| |___| |__  __ _| |
 / _` | / _ \ '_ \/ _` | |
 \__, |_\___/_.__/\__,_|_|
 |___/                    

*/

var globalmenu = {};
var currenturlstr = '';
var baseurl = '';
function _getbaseurl(input) {
    if(String(input).indexOf('http')>-1) { //console.log(input)
        return input;
    } else {
        if(input==undefined) return '';
        //return baseurl + input;
        return input;
    }
}
function _encodehtml(input) {
    return input
        .replace(/&/g, '＆amp;')
        //.replace(//g, '＆gt;')
        .replace(/"/g, '＆quot;')
        .replace(/'/g, '＆apos;');
}
function _decodehtml(input) {
    return input.replace(/＆apos;/g, "'")
        .replace(/＆quot;/g, '"')
        .replace(/＆gt;/g, '>')
        .replace(/＆lt;/g, '<')
        .replace(/＆amp;/g, '&');
}
function _formatnumber(x) {
    x = x.toString();
    var pattern = /(-?\d+)(\d{3})/;
    while (pattern.test(x))
        x = x.replace(pattern, "$1,$2");
    return x;
}
function _checkblank(obj, msg){
    if(obj.val()=='') {
        obj.parent().find('.msg.error').remove();
        obj.parent().safeAppend('<span class="msg error">'+msg+'</span>');
        return false;
    }
    return true;
}
function _checknumber(obj, msg) {
    if(isNaN(parseFloat(obj.val()))) {
        obj.parent().find('.msg.error').remove();
        obj.parent().safeAppend('<span class="msg error">'+msg+'</span>');
        return false;
    }
    return true;
}
function _getlang() {
    if($('body').hasClass('lang-en')) return 'en';
    else return 'tw';
}
function _reverselang(input) {
    if(input=='zh-tw') return 'en-us';
    else return 'zh-tw';
}
function _getparam(input, from) {
    var tmp = from.split('&');
    for(var n=0; n<tmp.length; n++) {
        var tmp2 = tmp[n].split('=');
        if(tmp2[0]==input) return tmp2[1];
    }
    return false;
}
function _setloader() {
    $('body').safeAppend('<div class="loader"></div>');
    setTimeout(function() {
        _removeloader();
    }, 5000);
}
function _removeloader() {
    $('body .loader').remove();
}
function _setloading(obj) {
    //return;
    $(obj).css({height:$(window).width()*.25});
    $(obj).safeAppend('<div class="loader"></div>');
}
function _removeloading(obj) {
    $(obj).css({height:'auto'});
    $(obj).find('.loader').remove();
}
function _mlink_checkclass(obj) {
    var tmp = '';
    if(obj.menu!=undefined && obj.link==undefined) tmp = 'nolink';
    if(obj.menu!=undefined && obj.link=='') tmp = 'nolink';
    if(obj.link!=undefined && obj.link!='' && String(obj.link).indexOf('html')>0 ) tmp = '';
    if(String(_getbaseurl(obj.link)).indexOf('http')>-1) tmp += ' outlink';
    return tmp;
}
function _mlink_link(obj) {
    if(obj.link!=undefined) {
        var tmp = ' title="'+obj.title+_addouttxt2(obj)+'" href="'+obj.link+'" ';

        if((obj.blank == true) ||
            (obj.external == true)) {
            tmp += 'target="_blank" ';
        }
        return tmp;
    } else {
        return '';
    }
}
function _mlink_sideli(obj) {
    var tmp = 'nolink ';
    if(obj.link!=undefined && obj.link!='') tmp = ' withlink ';
    if(obj.menu!=undefined) tmp += ' withgroup';
    return tmp;
}
function _addouttxt(obj) {
    if(obj.link!=undefined && obj.link.indexOf('http')>-1 ) {
        var tmp = ((_onlang=='zh-tw')?'(另開視窗)':'(Open external link)');
        return obj.title;//+tmp;
    } else {
        return obj.title;
    }
}
function _addouttxt2(obj) {
    if(obj.link!=undefined && obj.link.indexOf('http')>-1 ) {
        var tmp = ((_onlang=='zh-tw')?'(另開視窗)':'(Open external link)');
        return tmp;
    } else {
        return ''; //obj.title;
    }
}
function _caltotalgapheight() {
    $('.megamenu').find('.con').each(function() {
        var total = $(this).find('a').length;
        var _gap = $(window).width()*0.03;
        var h = total/4 * _gap;
        var withad = false;
        if( $(this).find('.ad').length>0 ) withad = true;

        if($(window).width()<641 && !$('body').hasClass('accessmodexx') ) {
            var ww = 100 / $(this).find('.tabset .tab').length;
            $(this).find('.tabset .tab').css({width:ww+'%', left:$(window).width() });
            $(this).find('.con').css({height:$(window).height() - ($(this).find('.tabset').height()+140) });
        } else {

            h = total/2 * _gap;
                var coll = 4;
                    if(withad) coll = 3;
                    if($(window).width()<1090) {
                        coll = 3;
                        if(withad) coll = 2;
                    }

                var th = total*50;
                    th = 0;
                    $(this).find('li, .gap').each(function() {
                        th += $(this).height();
                    });
                    h = th / coll;
                    h += 200;//增加上下留白空間
                    //console.log( 'on >48', total, h)
            //}
            if(h<180) h = 180;
            if( $(this).find('.ad.larger').length>0 && $(this).find('.ad.larger').height()!=undefined && $(this).find('.ad.larger').height()>0) {
                //console.log(h, $(this).find('.ad.larger').height() )
                if( ($(this).find('.ad.larger').height()+40)>h ) {
                    h = $(this).find('.ad.larger').height()+40;
                }
            }
        }
        $(this).find('ul').css({maxHeight:h, height:h});
        $(this).attr('data-total', total);
        $(this).attr('data-h', h);
        $(this).find('a,button').last().addClass('conlast');
    });
}
function _init_menu() {

    // getdata
        function _setmenu(data) {
            var d = data.data; 
                globalmenu = d;
            var b = '';
            for(var n=0; n<d.length; n++) {
                b += '<li class="onlevel1">';
                    b += '<a class="menu level1" data-code="'+d[n].code+'" href="#" alt="'+d[n].title+'">'+d[n].title+'</a>';

                        b += '<div class="megatabset tabset tabset'+(n+1)+'">';
                        for(var m=0; m<d[n].menu.length; m++) {
                            b += '<a href="#" class="level2 tab tab'+(m+1)+'" alt="'+d[n].menu[m].title+'">'+d[n].menu[m].title+'</a>';
                        }
                            b += '<a href="#" class="btn-close" title="'+((_onlang=='zh-tw')?'關閉選單':'Close megamenu')+'" ></a>';
                        b += '</div>';

                    b += '<div class="megamenu mega'+(n+1)+'">';
                        b += '<a href="#" class="btn-prev"></a>';
                        
                        // content
                        for(var m=0; m<d[n].menu.length; m++) {
                            var dd = d[n].menu[m].menu; 
                            var ad = d[n].menu[m].ad; 
                            b += '<div class="con con'+(m+1)+'" data-order="'+(m+1)+'">';
                                b += '<ul>';
                                b += '<a href=""></a>';
                                
                                //console.log('2.', dd);
                                if(dd!=undefined) {

                                    for(var m1=0; m1<dd.length; m1++) {
                                        // level3
                                        var ongap = false;
                                        if(dd[m1].menu!=undefined) {
                                            var ll = '';
                                                b += '<li><a class="level3 '+_mlink_checkclass(dd[m1])+'" '+_mlink_link(dd[m1])+' alt="'+dd[m1].title+'">'+dd[m1].title+'</a></li>';

                                            ongap = true;
                                            for(var m2=0; m2<dd[m1].menu.length; m2++) {
                                                // level4
                                                b += '<li><a class="level4 '+_mlink_checkclass(dd[m1].menu[m2])+'" '+_mlink_link(dd[m1].menu[m2])+' alt="'+dd[m1].menu[m2].title+'">'+dd[m1].menu[m2].title+'</a></li>';
                                                if(dd[m1].menu[m2].menu!=undefined) {
                                                    for(var m3=0; m3<dd[m1].menu[m2].menu.length; m3++) {
                                                        // level5
                                                        b += '<li><a class="level5 '+_mlink_checkclass(dd[m1].menu[m2].menu[m3])+'" '+_mlink_link(dd[m1].menu[m2].menu[m3])+' alt="'+dd[m1].menu[m2].menu[m3].title+'">'+dd[m1].menu[m2].menu[m3].title+'</a></li>';
                                                    }
                                                }
                                            }
                                        } else {
                                            b += '<li><a class="level3 '+_mlink_checkclass(dd[m1])+' " '+_mlink_link(dd[m1])+' alt="'+dd[m1].title+'">'+dd[m1].title+'</a></li>';
                                        }
                                        if(ongap) b += '<span class="gap"></span>';
                                    }

                                }
                                if(ad!=null && ad!=undefined) {
                                    if(ad.length>0) {
                                        b += '<span class="ad larger">';
                                            for(var m3=0; m3<ad.length; m3++) {
                                                b += '<a class="ad-link" ' + _mlink_link(ad[m3]) + '>';
                                                    b += '<img src="'+ad[m3].image+'">';
                                                    b += '<strong>'+ad[m3].title+'</strong>';
                                                    b += '<p>'+ad[m3].content+'</p>';
                                                b += '</a>';
                                            }
                                        b += '</span>';
                                    }
                                }

                                b += '</ul>';
                            b += '</div>';
                        }

                        

                b += '</li>';
            }
            //b += '</ul>';
            $('.fullmenu .nav.fullh li').remove();
            $('.fullmenu .nav.fullh').safePrepend(b);
            $('.fullmenu').safeAppend('<a class="btn-next"></a>');
            $('.fullmenu').addClass('disabled');


            setTimeout(function() {
                $('.fullmenu').removeClass('disabled');
                _settopmenuevent();
            }, 1000);



            // event

                var onhoverint;
                var onhovert = 0;
                var onmega = false;
                function _closemenu() {
                    clearTimeout(onhoverint);
                    clearTimeout(onhoverint);
                    onmega = false;
                    $('html,body').removeClass('noscroll');
                    $('.overlay').hide();
                    $('.header .nav li').removeClass('hover');
                    $('.header').removeClass('hover');
                    $('.megamenu').removeClass('hover');
                    $('.megatabset').removeClass('hover');
                }
                function _resize() {
                    _onapp = _checkapp();
                    if(_onapp) {
                        $('.header .nav.fullh .cover').hide();
                        $('body').addClass('onapp');
                    } else {
                        $('.header .nav.fullh .cover').show();
                        $('body').removeClass('onapp');
                    }
                    if($(window).width()<641 && !$('body').hasClass('accessmode') ) {
                        $('.header .nav').hide();
                        $('.header').find('.nav.fullh .topright .nav').show();
                        $('.megamenu .tabset').css({
                            left:$(window).width(),
                        });
                        $('.fullmenu').removeClass('switcher');
                    } else {
                        $('.header .nav').show().css({display:'flex', left:0,});
                        $('.header').find('.nav.fullh .topright .nav').hide();
                        $('.header>.megatabset').remove();
                        $('.megamenu .tabset').css({
                            top:$('header').height()+$(window).width()*.005,
                            left:0, display:'flex',
                        });

                        // switch
                            var allowswitch = false;
                            var _zhw = 1500;//1060;
                            var _enw = 1640;//1400;
                            if($('body').hasClass('lang-zh-tw') && $(window).width()<_zhw) { allowswitch = true; }
                            if($('body').hasClass('lang-en-us') && $(window).width()<_enw) { allowswitch = true; }
                            if(allowswitch && $(window).width()>640) {
                                $('.fullmenu').addClass('switcher');
                            } else {
                                $('.fullmenu').removeClass('switcher');
                            }

                        // menu
                        _caltotalgapheight();
                    }
                }
                _caltotalgapheight();


                function _rundebug(input) {
                    $('body .debug').remove();
                    var b = '<div class="debug">'+input+'</div>';
                    $('body').append(b);
                }
                function _openmm(obj, num) {
                    $('.overlay').show();
                    $('.header .nav li').removeClass('hover');
                    $('.header').addClass('hover');
                    obj.addClass('hover');
                    $('.megamenu').removeClass('hover');
                    $('.mega'+num).addClass('hover');
                    $('.megatabset').removeClass('hover');
                    $('.megatabset.tabset'+num).addClass('hover').show();
                    onmega = true;
                    //if(mouseposy<92) 
                        _caltotalgapheight();
                }

                var allowcounting = true;
                var allowcounter = 0;
                var allowint;
                var mouseposy;
                $(window).mousemove(function(e) {
                    mouseposy = e.clientY;
                    if($(window).width()<640) return;
                    if(e.clientY<90 && e.clientY>50) {
                        if(!allowcounting) return;
                    } else {
                        allowcounter = 0;
                        allowcounting = true;
                        clearTimeout(allowint);
                        $('.header .nav.fullh .cover').show();
                    }
                });
                $('.header .nav').mousedown(function(e) {
                    if(mouseposy<92 || e.clientY<92) {
                        _caltotalgapheight();
                    }
                });
                $('.level1').on('mousedown, click, touchstart', function(e) {
                    if(mouseposy<92) {
                        _caltotalgapheight();
                    }
                });
                $('.header .nav li .level1').mouseover(function(e) {
                    
                    if($(window).width()<641 && !$('body').hasClass('accessmode') ) {
                        // mobile m
                        e.preventDefault();

                        $('.header>.megatabset').remove();
                        $('.header>.megamenu').remove();

                        $('.megamenu').removeClass('hover');
                        var num = $(this).closest('li').index()+1;
                        $('.mega'+(num)).addClass('hover').show();
                        $(this).find('.megatabset').hide();
                        $('.header').safeAppend( $('.mega'+(num)).clone() );
                        $('.header').safeAppend( $('.megatabset.tabset'+(num)).clone() );
                
                        $('.header>.megamenu').addClass('top');
                        $('.header>.megatabset').addClass('top');
                            var ttotal = $('.header>.megatabset.top .tab').length;
                            $('.header>.megatabset.top .tab').css({width: (100/ttotal)+'%' });
                        $('.header>.megamenu .btn-prev').click(function() {
                            TweenMax.to($('.header .nav'), .7, {left:0, ease:Expo.easeInOut});
                            TweenMax.to($('.header>.megamenu.top'), .7, {left:$(window).width(), ease:Expo.easeInOut});
                            TweenMax.to($('.header>.megatabset.top'), .7, {left:$(window).width(), ease:Expo.easeInOut,
                                onComplete:function() {
                                    $('.header>.megamenu.top').remove();
                                    $('.header>.megamenu.top .btn-prev').hide();
                                }
                            });
                        });
                        // animation
                            TweenMax.fromTo($('.header .nav'), .7, {left:0}, {left:-$(window).width(), ease:Expo.easeInOut});
                            TweenMax.fromTo($('.header>.megamenu.top'), .7, {left:$(window).width()}, {left:0, ease:Expo.easeInOut});
                            TweenMax.fromTo($('.header>.megatabset.top'), .7, {display:'flex', left:$(window).width()}, {left:0, ease:Expo.easeInOut});
                            $('.header>.megatabset.top').show();

                        $('.header>.megatabset.top').find('.tab').click(function() {
                            $('.header>.megamenu.top').find('.con').hide();
                            $('.header>.megamenu.top').find('.con').eq( $(this).index() ).show();
                            $('.header>.megatabset.top').find('.tab').removeClass('selected');
                            $(this).addClass('selected');
                        });

                    } else {
                        e.preventDefault();
                        var num = ($(this).parent().index()+1);
                        var obj = $(this).parent();
                        _openmm(obj, num);
                    }
                });
                // $('.header .nav li').find('a').each(function() {
                //     if( String($(this).attr('href')).indexOf('http')>-1 ) {
                //         $(this).attr('target', '_blank');
                //     }
                // });
                $('.header .nav>li>a').click(function(e) {
                    e.preventDefault();
                    if(mouseposy<92) {
                        var num = ($(this).parent().index()+1);
                        var obj = $(this);
                        _openmm(obj, num);

                    }
                });
                $('.fullmenu .btn-next').click(function() {
                    var tx = $('.nav.fullh').position().left;
                    if(!$('.fullmenu .btn-next').hasClass('open')) {
                        //tx = 0 - $('.fullmenu').width()*.8;
                        tx -= $('.fullmenu').width()*.9;
                        if( Math.abs(tx)>($('.nav.fullh').width()-$('.fullmenu').width()*.8) ) {
                            $('.fullmenu .btn-next').addClass('open');
                        }
                    } else {
                        tx = 0;
                        $('.fullmenu .btn-next').removeClass('open');
                    }
                    TweenMax.to($('.fullmenu .nav'), .5, {left:tx });
                });
                $('.header .btn-menu').click(function(e) {
                    $('.header').addClass('hover');
                    if(!$('.header .nav').hasClass('open')) {
                        $('body').addClass('noscroll');
                        $(this).addClass('open');
                        $('.header').addClass('open');
                        $('.header .nav').slideDown('fast');
                        $('.header .nav').show();
                        $('.header .nav').addClass('open');
                    } else {
                        $(this).removeClass('open');
                        $('.header').removeClass('open');
                        //$('.header .nav').slideUp();
                        $('.header .nav').hide();
                        $('.header .nav').removeClass('open');
                        $('html,body').removeClass('noscroll');
                    }
                });
                $('.megamenu, .header').mouseleave(function() {
                    //_closemenu();
                });
                $('.header .nav').mouseleave(function() {
                    _closemenu();
                });
                $('.overlay').on('mousedown, mousemove, touchend', function() {
                    _closemenu();
                });
                $('.megatabset .btn-close').click(function(e) {
                    e.preventDefault();
                    $(this).closest('li').find('.megamenu').removeClass('hover').hide();
                    $(this).closest('li').find('.megatabset').removeClass('hover').hide();
                    $('.header .nav li').removeClass('hover');
                    $('html,body').removeClass('noscroll');
                    $('.overlay').hide();
                });
                $('.megatabset').each(function() {
                    var obj = $(this).parent().find('.megamenu');
                    $(this).parent().find('.megamenu .con').hide();
                    $(this).parent().find('.megamenu .con').first().show();
                    $(this).find('.tab').first().addClass('selected');
                    $(this).find('.tab').click(function() {
                        var total = $(this).find('a').length;
                        obj.find('.con').hide();
                        obj.find('.con').eq( $(this).index() ).show();
                        if( obj.find('.con').eq( $(this).index() ).find('.group').length>0 ) {
                            var currenth = parseInt(obj.find('.con').eq( $(this).index() ).find('ul').css('maxHeight'));
                            var theh = ( obj.find('.con').eq( $(this).index() ).find('.group').height() );
                            if((theh+80)>currenth) {
                                //console.log( '重新計算高度', currenth, theh );
                                obj.find('.con').eq( $(this).index() ).find('ul').css({maxHeight:theh + 80});
                            }
                        }
                        $(this).parent().find('.tab').removeClass('selected');
                        $(this).addClass('selected');
                        _caltotalgapheight();

                    });
                });

                function _checkapp() {
                    let check = false;
                    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
                    return check;
                }
                var _onapp = _checkapp();
                _resize();
                $(window).resize(function() {_resize();});

                // after menu, set
                var url = document.location.pathname;
                currenturlstr = url.substr( 6 );
                if(currenturlstr.indexOf('?')>0)
                    currenturlstr = currenturlstr.substr( 0, parseInt(currenturlstr.indexOf('?')) );
                _init_scroll();
                //_init_accessbility();
                _init_runsidemenu();
        }

        function _getlangjson(input) {
            if(input=='zh-tw') {
                _get_json(_setmenu, _menulink_tw);
            } else {
                _get_json(_setmenu, _menulink_en);
            }
            _setbodylang(_onlang);
        }
        function _gohome() {
            document.location = encodeURI('/'+_onlang+'/index.html');
        }

    // init

        $('a').click(function(e) {if($(e.target).attr('href')=='') e.preventDefault();});
        $('.btn-home').click(function() { _gohome(); });
        $('.header').find('.logo').click(function() { _gohome(); });
        if( $('section.title').find('.formblock').length<1 ) {
            $('section.title').safeAppend('<form class="formblock flex open"></form>');
        }
        var megah = $(window).height()*.55;
        _getlangjson(_onlang);


        function _settopmenuevent() {
            $('.btn-menuchange').click(function(e) {
                e.preventDefault();
                var metastr = $('meta[name="language-toggle"]').attr('content');
                if(metastr!=undefined) {
                    document.location = metastr;
                    return;
                }

                var tmp = ( String(document.location).substr(String(document.location).indexOf('?')));
                    if(tmp.substr(0,1)!='?') tmp = '';
                var str = '/'+_reverselang(_onlang)+''+String(document.location.pathname).substr(6)+tmp;
                document.location = encodeURI(str);
            });
        }
}
function _setbodylang(input) {
    $('body').removeClass('lang-en-us lang-zh-tw');
    $('body').addClass('lang-'+input);
}






var onmenu = 0;
function _init_sidemenu(num) {
    // init
    $('body').addClass('section'+num);
    $('body').addClass('sidemenuopen');
    onmenu = num;
}
function _getcurrentsection() {
    var tmp = currenturlstr.substr(1);
    var tmp2 = tmp.substr(0, tmp.indexOf('/') );
    for(var n=0; n<globalmenu.length; n++) {
        //console.log(tmp2, globalmenu[n].code)
        if(tmp2==globalmenu[n].code) {
            return (n+1);
        }
    }
    return 0;
}
function _init_runsidemenu() {

    // getdata
        function _setmenu(d, num) {
            //console.log(num, d )

            if(num==undefined) num = 1;
            if(num==-1) num = 11;

            var b = '';
            if(lan==='zh') {
                b += '<div class="btn-show">開啟側欄選單</div>';
                b += '<a href="#accesskey-l" accesskey="l" class="accesskey" title="側欄選單區 (Alt-L)">:::</a>';
            }
            else {
                b += '<div class="btn-show">Open side menu</div>';
                b += '<a href="#accesskey-l" accesskey="l" class="accesskey" title="Side Menu (Alt-L)">:::</a>';              
            }
            if(d[num]!=undefined) {
                b += '<div class="nav nav'+(num+1)+'" data-title="'+d[num].title+'" data-url="'+d[num].link+'">';
                for(var n=0; n<d.length; n++) {
                    if(n==num) {
                            
                        // content
                        for(var m=0; m<d[n].menu.length; m++) {
                            b += '<strong>';
                                b += d[n].menu[m].title+'</strong>';
                            var dd = d[n].menu[m].menu; 
                                //console.log( dd );
                            b += '<div class="con con'+(m+1)+'">';
                                b += '<ul>';
                                //b += '<a href=""></a>';

                                if(dd!=undefined) {

                                    for(var m1=0; m1<dd.length; m1++) {
                                        //console.log( dd[m1].menu.length )
                                        // level3
                                        var ongap = false;
                                        var ex = ( (dd[m1].external==true)?' outlink" target="_blank':'' );
                                        if(dd[m1].menu!=undefined) {
                                            b += '<li><ol class="group group3">';
                                                b += '<a class="btn-arrow"><span class="img"></span></a>';
                                                b += '<li class="level3 '+_mlink_sideli(dd[m1])+'" ><a class="'+_mlink_checkclass(dd[m1])+'" '+_mlink_link(dd[m1])+'>'+dd[m1].title+'</a></li>';

                                                ongap = true;
                                                for(var m2=0; m2<dd[m1].menu.length; m2++) {
                                                    // level4
                                                    b += '<li class="level4 '+_mlink_sideli(dd[m1].menu[m2])+'"><a class="'+_mlink_checkclass(dd[m1].menu[m2])+'" '+_mlink_link(dd[m1].menu[m2])+' alt="'+dd[m1].menu[m2].title+'">'+dd[m1].menu[m2].title+'</a></li>';
                                                    if(dd[m1].menu[m2].menu!=undefined) {
                                                        b += '<span class="group group4">'
                                                        for(var m3=0; m3<dd[m1].menu[m2].menu.length; m3++) {
                                                            // level5
                                                            b += '<li class="level5"><a '+_mlink_link(dd[m1].menu[m2].menu[m3])+' alt="'+dd[m1].menu[m2].menu[m3].title+'">'+dd[m1].menu[m2].menu[m3].title+'</a></li>';
                                                        }
                                                        b += '</span>';
                                                    }
                                                }
                                            b += '</ol>';
                                        } else {
                                            b += '<li class="level3 '+_mlink_sideli(dd[m1])+'" ><a class="'+_mlink_checkclass(dd[m1])+'" '+_mlink_link(dd[m1])+'>'+dd[m1].title+'</a></li>';
                                        }
                                        if(ongap) b += '<span class="gap"></span>';
                                    }

                                }
                                b += '</ul>';
                            b += '</div>';
                        }

                    }
                }
            }
            b += '</div>';
            $('.sidemenu').empty().safeAppend( b );
            $('.sidemenu').css({height: $('.container').height() - $('.footer').height() + (16*13.5) });
            if(!$('header').hasClass('home'))
                $('.mega'+(num+1)).closest('li').addClass('selected');
            




            // event
                $('.sidemenu').find('.level4, .level5').each(function() {
                    $(this).hide();
                });
                var bb = '';
                var allowbb = true;
                function _getbread(obj) {
                    if(!allowbb) return;
                    bb += '<a class="btn-sidemenu" title="'+((_onlang=='zh-tw')?'開啟側選單':'Open Sidemenu')+'" href=""></a>';
                    /*1*/ bb += '<a role="button" class="nolink" href="'+obj.closest('.nav').attr('data-link')+'" alt="'+obj.closest('.nav').attr('data-title')+'">'+obj.closest('.nav').attr('data-title')+'</a>';
                    /*2*/ bb += '<a role="button" class="nolink" href="'+obj.closest('.con').prev().attr('href')+'" alt="'+obj.closest('.con').prev().text()+'">'+obj.closest('.con').prev().text()+'</a>'; //listnumber
                    /*3*/ 
                        if(obj.parent().hasClass('level3') && obj.parent().find('.group4').length>0 ) {
                            var strtmp = '';
                            if(obj.closest('.group3').find('.level3').attr('href')=='' || obj.closest('.group3').find('.level3').attr('href')==undefined) {
                                strtmp = ' class="nolink" '; } else { strtmp = ''; }
                            bb += '<a role="button"'+strtmp+' href="'+obj.closest('.group3').find('.level3').attr('href')+'" alt="'+obj.closest('.group3').find('.level3').text()+'">'+obj.closest('.group3').find('.level3').text()+'</a>'; //listnumber
                        }
                    /*4*/
                        if(obj.parent().hasClass('level4') && obj.closest('.group3').find('.level3').text()!='' ) {
                            var strtmp = '';
                            if(obj.closest('.group4').find('.level4').attr('href')=='' || obj.closest('.group4').find('.level4').attr('href')==undefined) {
                                strtmp = ' class="nolink" '; } else { strtmp = ''; }
                            bb += '<a role="button"'+strtmp+' href="'+obj.closest('.group4').find('.level4').attr('href')+'" alt="'+obj.closest('.group3').find('.level3').text()+'">'+obj.closest('.group3').find('.level3').text()+'</a>';
                        }
                        if(obj.parent().hasClass('level5') && obj.parent().parent().hasClass('group4') ) {
                            //console.log('got 54', obj.closest('.group3').find('.level3 > a').text() );
                            var strtmp = '';
                            if(obj.closest('.group3').find('.level3 > a').attr('href')=='' || obj.closest('.group3').find('.level3 > a').attr('href')==undefined) {
                                strtmp = ' class="nolink" '; } else { strtmp = ''; }
                            bb += '<a role="button"'+strtmp+' href="'+obj.closest('.group3').find('.level3>a').attr('href')+'" alt="'+obj.closest('.group3').find('.level3>a').text()+'">'+obj.closest('.group3').find('.level3>a').text()+'</a>';
                        }

                    /*5*/
                        if(obj.parent().hasClass('level5') && obj.closest('.group4').prev().find('a').text()!='' ) {
                            var strtmp = '';
                            if(obj.closest('.group4').prev().find('a').attr('href')=='' || obj.closest('.group4').prev().find('a').attr('href')==undefined) {
                                strtmp = ' class="nolink" '; } else { strtmp = ''; }
                            bb += '<a role="button"'+strtmp+' href="'+obj.closest('.group4').prev().find('a').attr('href')+'" alt="'+obj.closest('.group4').prev().find('a').text()+'">'+obj.closest('.group4').prev().find('a').text()+'</a>';
                        }
                        bb += '<a role="button" href="'+obj.attr('href')+'" alt="'+obj.text()+'">'+obj.text()+'</a>';


                    /*hint*/
                        if(!_s_get('breadcrumbhintobjshow'))
                            bb += '<div class="hintobj">'+((_onlang=='zh-tw')?'點擊箭頭符號<br>即可收合側選單':'Click on icon to<br>toggle sidemenu')+'</div>';

                        allowbb = false;

                    return bb;
                }
                function _runselectside(str) {
                    var nowstr = String($(this).attr('href'));
                    var tmpstr = nowstr.substr(0, nowstr.lastIndexOf('/'));
                    var metastr = $('meta[name="path"]').attr('content');
                    $('.sidemenu').find('a').each(function() {
                        
                        if(allowbb) {
                            
                            if(metastr!=undefined) {
                                if( metastr==nowstr ) {
                                    $(this).closest('.group3').addClass('open');
                                    $(this).closest('.group4').addClass('open');
                                    $(this).addClass('selected');
                                    opened = true;
                                    bb = _getbread($(this));
                                } else {
                                    if(String($(this).attr('href')) == metastr ) {
                                        $(this).closest('.group3').addClass('open');
                                        $(this).closest('.group4').addClass('open');
                                        $(this).addClass('selected');
                                        opened = true;
                                        bb = _getbread($(this));
                                    }
                                }
                            } else if( String($(this).attr('href')).indexOf(str)>0 ) {
                                $(this).closest('.group3').addClass('open');
                                $(this).closest('.group4').addClass('open');
                                $(this).addClass('selected');
                                opened = true;
                                bb = _getbread($(this));
                            }
                            if( String($(this).attr('href')).indexOf('http')>-1 ) {
                                $(this).attr('target', '_blank');
                            }
                            if($(this).hasClass('selected')) {
                                // 設定自動滾動
                                    var scrolltt = $(this).closest('li').position().top;
                                    if($(this).closest('.group4').length>0) scrolltt += $(this).closest('.group4').position().top;
                                    if($(this).closest('.group3').length>0) scrolltt += $(this).closest('.group3').position().top;
                                    if($(this).closest('.con').length>0) scrolltt += $(this).closest('.con').position().top;
                                    scrolltt += $(this).closest('.sidemenu').position().top;
                                    scrolltt += 100;
                                    //console.log( scrolltt, $(window).height()-140 )
                                        if(scrolltt<$(window).height()-140) return;
                                        TweenMax.to($('.sidemenu'), .7, {scrollTop:scrolltt, ease:Expo.easeInOut});
                            }
                        }
                    });
                    $('.breadcrumb').empty().safeAppend( bb );
                    $('.breadcrumb .hintobj').click(function() {
                        $('.breadcrumb .hintobj').remove();
                        _s_set('breadcrumbhintobjshow', false);
                    });
                    // check if breadcrumb
                    if(bb=='') {
                        $('body').removeClass('sidemenuopen');
                        $('body').addClass('nosidemenu');
                    }
                }

                var opened = false;
                _runselectside(currenturlstr);
                if(!opened) {
                    var newstr = currenturlstr.substr(0, currenturlstr.lastIndexOf('/') );
                }


                function _closesidemenu() {
                    $('.sidemenu').find('.nav').hide();
                    $('.breadcrumb .btn-sidemenu').removeClass('open');
                    $('body').removeClass('sidemenuopen');
                }
                function _opensidemenu() {
                    $('.sidemenu').find('.nav').show();
                    $('.breadcrumb .btn-sidemenu').addClass('open');
                    $('body').addClass('sidemenuopen');
                }
                $('.breadcrumb .btn-sidemenu').click(function(e) {
                    //$('.sidemenu').find('.btn-show').click(function() {
                    if( $('body').hasClass('sidemenuopen') ) {
                        _closesidemenu();
                        _s_set('sidemenuopen', 'false');
                    } else {
                        _opensidemenu();
                        _s_set('sidemenuopen', 'true');
                    }
                    e.preventDefault();
                });
                $('.breadcrumb a').click(function(e) {
                    if( $(this).hasClass('nolink') ) {
                        e.preventDefault();
                    }
                });
                $('.sidemenu').find('ol .btn-arrow').click(function() {
                    if( $(this).parent().hasClass('open') ) {
                        $(this).parent().removeClass('open');
                    } else {
                        $(this).parent().addClass('open');
                    }
                });

                $('.sidemenu').scroll(function() {
                    _s_set('sidemenupos', $('.sidemenu').scrollTop() );
                });

                
                if(_s_get('sidemenuopen')=='true' ) {
                    if(!$('body').hasClass('nosidemenu'))
                        _opensidemenu();
                } else {
                    _closesidemenu();
                }
        }

    // init
        var num = _getcurrentsection();
        if(num==0) num = 12;
        onmenu = num;

        // 特殊案例
        // if(currenturlstr=='/bond.html') { num = 4; onmenu = 4; }
        if(num!=0 && !$('.header').hasClass('home') )
            $('body').addClass('section'+num);

        _setmenu( globalmenu, num-1 );

}
function _init_sitemap(obj) {

    // getdata
        function _setmenu(d) {
            var b = '';
            for(var n=0; n<d.length; n++) {
                b += '<div class="group1 set'+(n+1)+'">';
                    b += '<h3 class="menuset'+(n+1)+'">'+d[n].title+'</h3>';
                    b += '<div class="group2">';
                    for(var m=0; m<d[n].menu.length; m++) {
                        b += '<div class="group3">';
                            b += '<strong>'+(m+1)+'.'+d[n].menu[m].title+'</strong>';
                            var dd = d[n].menu[m].menu; 
                                //console.log( dd );
                            b += '<div class="con con'+(m+1)+'">';
                                b += '<ul>';
                                b += '<a href="" ></a>';
                                    for(var m1=0; m1<dd.length; m1++) {
                                        // level3
                                        var ongap = false;
                                        var ex = ( (dd[m1].external==true)?' outlink" target="_blank':'' );
                                        if(dd[m1].menu!=undefined) {
                                            b += '<li><ol class="group">';
                                                b += '<a class="btn-arrow"><span class="img"></span></a>';
                                                b += '<li class="level3 '+_mlink_sideli(dd[m1])+'" ><a class="'+_mlink_checkclass(dd[m1])+'" '+_mlink_link(dd[m1])+'>'+_addouttxt(dd[m1])+'</a></li>';

                                                ongap = true;
                                                for(var m2=0; m2<dd[m1].menu.length; m2++) {
                                                    // level4
                                                    b += '<li class="level4">';
                                                    if(dd[m1].menu[m2].menu!=undefined) {
                                                        b += ''+dd[m1].menu[m2].title+'';
                                                        for(var m3=0; m3<dd[m1].menu[m2].menu.length; m3++) {
                                                            // level5
                                                            b += '<a class="level5 '+_mlink_checkclass(dd[m1].menu[m2].menu[m3])+'" '+_mlink_link(dd[m1].menu[m2].menu[m3])+'>'+_addouttxt(dd[m1].menu[m2].menu[m3])+'</a>';
                                                        }
                                                    } else {
                                                        b += '<a class="'+_mlink_checkclass(dd[m1].menu[m2])+'" '+_mlink_link(dd[m1].menu[m2])+'>'+_addouttxt(dd[m1].menu[m2])+'</a>';
                                                    }
                                                    b += '</li>';
                                                }
                                            b += '</ol>';
                                        } else {
                                            b += '<li class="level3 '+_mlink_sideli(dd[m1])+'" ><a class="'+_mlink_checkclass(dd[m1])+'" '+_mlink_link(dd[m1])+'>'+_addouttxt(dd[m1])+'</a></li>';
                                        }
                                        if(ongap) b += '<span class="gap"></span>';
                                    }
                                b += '</ul>';
                            b += '</div>';
                        b += '</div>';
                    }
                    b += '</div>';
                b += '</div>';
            }
            obj.empty().safeAppend(b);

            // event
        }

    // init
        setTimeout(function() {
            _setmenu( globalmenu );
        }, 500);
}
function _init_fullscreen() {
    $('body').addClass('fullscreen');
    $('.header').safeAppend($('.container .title'));
    $('.container>section>.row').safePrepend($('.header .title .tabset'));
}
function _init_form() {
    $('.formblock .row').hide();
    $('.formblock .btn-open').removeClass('btn');
    $('.formblock .btn-open').click(function() {
        if( $('.formblock').hasClass('open') ) {
            $('.formblock').removeClass('open');
            $('.formblock .row').slideUp();
            _s_set('formopen', false);
        } else {
            $('.formblock').addClass('open');
            $('.formblock .row').slideDown();
            _s_set('formopen', true);
        }
    });
    //if(String(_s_get('formopen'))=='true') {
        $('.formblock').addClass('open');
        $('.formblock .row').show();
    //}

    // additional form
        $('.topbtnrow .btn-arrow-prev').click(function() {
            const refPath = document.referrer?new URL(document.referrer).pathname:'';
            const listPath = $('meta[name="path"]').attr('content');
            if(listPath===refPath)
                history.back();
            else
                document.location.href = listPath; 
        });
}
function _init_sticky() {}
function _init_quicktab() {

    // center quicklinkblock
        $('.quicktab_block').find('a').click(function(e) {
            var obj = $('.tablink[data-tab="'+$(this).attr('data-tab')+'"]');
            var y = obj.position().top + 160;
            TweenMax.to($('html,body'), .7, {scrollTop:y, ease:Expo.easeInOut});
            e.preventDefault();
        });

    // with tabcon
        if($('.tabcon').length>0) {
            if($('.tabcon').closest('.chartlistblock').length>0) {
                return;
            }
            $('.tabcon').hide();
            $('.tabcon1').show();
            $('.tabset .tab').click(function(e) {
                var num = $(this).index() + 1;
                $('.tabcon').hide();
                $('.tabcon'+num).fadeIn();
                $('.tabset .tab').removeClass('selected');
                $(this).addClass('selected');
                e.preventDefault();
            });
        }

    // with tabset as quicktab
        if($('.tabset').hasClass('quicktab')) {
            $('.tabset').find('.tab').click(function(e) {
                e.preventDefault();
                //console.log($(this).attr('data-tab'));return;
                var num = $(this).index();
                var obj = $('.tablink[data-tab="'+$(this).attr('data-tab')+'"]');
                var y = obj.position().top + $(window).width()*.1;
                TweenMax.to($('html,body'), .7, {scrollTop:y, ease:Expo.easeInOut});
                $('.tabset .tab').removeClass('selected');
                $('.tabset').each(function() { 
                    $(this).find('.tab').eq(num).addClass('selected');
                });
            });
        }

    // tabset scroll
        $('.title .tabset .tab').css({ width:$(window).width()*.12, width:180 });
        $('.title .tabset').css({overflowX:'auto'});
}
function _init_table() {}
function _init_tablesort() {
    function _tcheck() {
        if($('.container').find('table').width() > $('body').width() ) {
            $('.container').find('table').addClass('scroll');
            var obj = $('.hugetable').find('table').find('thead').clone().addClass('fixedtop').hide();
            $('.hugetable').safeAppend(obj);
        } else {
            $('.container').find('table').removeClass('scroll');
        }
        _sethw();
    }
    function _sethw() {
        var tmp = 0;
        var gap = $(window).width()*.011;
            if($(window).width()<641) gap = 13.5;
        $('.hugetable>thead').css({width:$('.hugetable>table').width() });
        $('.hugetable>thead tr').each(function() {
            var obj = $('.hugetable>table>thead>tr').eq($(this).index());
            $(this).find('th').each(function() {
                if($(window).width()<641) {
                    tmp += obj.find('th').eq($(this).index()).width()+gap;
                }
                $(this).css({ width:obj.find('th').eq($(this).index()).width()+gap });
            });
        });
        if($(window).width()<641) {
            $('.hugetable>thead').css({width:tmp });
        }
    }
    $(window).resize(function() {_tcheck();});
    _tcheck();


    // for sort
    // string line
        $('table').each(function() {
            if( $(this).attr('data-string')!=undefined ) {
                var num = $(this).attr('data-string');
                    if($(this).attr('data-string').indexOf(',')>0) 
                        ( $(this).attr('data-string') ).split(',');
                for(var n=0; n<num.length; n++) {
                    $(this).find('tr').each(function() {
                        $(this).find('td,th').eq( num[n]-1 ).addClass('string');
                    });
                }
            }
        });

    // string color
        $('table').each(function() {
            if( $(this).attr('data-color')!=undefined ) {
                var num = ( $(this).attr('data-color') ).split(',');
                    if($(this).attr('data-color').indexOf(',')>0) 
                        ( $(this).attr('data-color') ).split(',');

                for(var n=0; n<num.length; n++) {
                    $(this).find('tr').each(function() {
                        var sstr = Number( $(this).find('td').eq( num[n]-1 ).text() );
                        if(sstr>0) {
                            $(this).find('td,th').eq( num[n]-1 ).addClass('rise');
                        } else {
                            $(this).find('td,th').eq( num[n]-1 ).addClass('drop');
                        }
                    });
                }
            }
        });
}

function _set_tablesort(obj) {


    // for sort
    // string line
        $(obj).each(function() {
            if( $(this).attr('data-string')!=undefined ) {
                var num = $(this).attr('data-string');
                    if($(this).attr('data-string').indexOf(',')>0) 
                        ( $(this).attr('data-string') ).split(',');
                for(var n=0; n<num.length; n++) {
                    $(this).find('tr').each(function() {
                        $(this).find('td,th').eq( num[n]-1 ).addClass('string');
                    });
                }
            }
        });

    // excute; 
    $(obj).each(function() {
        // preset
            var tobj = $(this);
            var oncolumn = 0;

            function _runsort_textcheck(a, b) {
                var aa = Object(a[oncolumn]).data;
                var bb = Object(b[oncolumn]).data;
                if(aa === 'N/A') { return -1; }
                if(bb === 'N/A') { return 1; }
                if(aa === bb ) {
                    return 0;
                }

                return (aa<bb) ? -1 : 1;
            }
            function _runsort(a, b) {
                var aa = Object(a[oncolumn]).data;
                var bb = Object(b[oncolumn]).data;
                if( String(Number(aa))!='NaN' ) aa = Number(aa);
                if( String(Number(bb))!='NaN' ) bb = Number(bb);
                //console.log( aa, bb , '小於===>', aa < bb );
                if(aa === bb ) {
                    return 0;
                } else {
                    return (aa<bb) ? -1 : 1;
                }
            }
            function _getd() {
                var tmp = [];
                tobj.find('tbody').find('tr').each(function() {
                    var tmp1 = [];
                    $(this).find('td').each(function() {
                        var n = $(this).text().replaceAll(',', '');
                        var tmpd = {
                            type: 'string',
                            data: n,
                        };
                        tmp1.push( tmpd );
                    });
                    tmp.push(tmp1);
                });
                return tmp;
            }
            function _setformat(input) {
                if( input.type=='number' ) {
                    return _formatnumber(input.data);
                } else {
                    return input.data;
                }
            }
            function _resettable(d) {
                var count = 0;
                tobj.find('tbody').find('tr').each(function() {
                    var dd = d[count];
                    //console.log( $(this).index(), dd )
                    //if($(this).index()>0) {
                    $(this).find('td').each(function() {
                        $(this).text( _setformat(dd[$(this).index()]) );
                    });
                    //}
                    count++;
                });
            }


        // start setting
            $(this).find('th')
                .each(function() {
                    $(this).attr('data-sort', '0');
                    $(this).addClass('sort');
                })
                .click(function() {
                    oncolumn = $(this).index();
                    tobj.find('th').removeClass('up');
                    tobj.find('th').removeClass('down');
                    var direction = 'down';
                    if($(this).attr('data-sort')==0 || $(this).attr('data-sort')=='up') {
                        $(this).attr('data-sort', 'down');
                        $(this).addClass('down');
                        direction = 'down';
                    } else {
                        $(this).attr('data-sort', 'up');
                        $(this).addClass('up');
                        direction = 'up';
                    }
                    var d = _getd();
                        d.sort(_runsort_textcheck);
                        d.sort(_runsort);
                        if(direction=='up') {d.reverse();}

                    _resettable(d);
                });
    });
}
function _init_faq() {
    if($('.faqblock').length<1) return;
    $('.faqblock .item').each(function() {
        //$(this).find('>.con').attr('aria-expanded', 'false');
        $(this).find('>h3').attr('aria-expanded', 'false');
        $(this).find('>h3').attr('aria-label', '點擊或按Enter收合詳細內容');
        $(this).find('>h3').click(function(e) {
            e.preventDefault();
            if(!$(this).closest('.item').hasClass('open')) {
                $(this).closest('.item').addClass('open');
                $(this).closest('.item').find('>h3').attr('aria-expanded', 'true');
            } else {
                $(this).closest('.item').removeClass('open');
                $(this).closest('.item').find('>h3').attr('aria-expanded', 'false');
            }
        });
    });
    // event
    $('.btn-faq-openall').click(function() {
        if(!$('.btn-faq-openall').hasClass('disabled')) {
            $('.btn-faq-openall').addClass('disabled');
            $('.faqblock .item').each(function() {
                $(this).closest('.item').addClass('open');
                $(this).closest('.item').find('.con').attr('aria-expanded', 'true');
            });
        } else {
            $('.btn-faq-openall').removeClass('disabled');
            $('.faqblock .item').each(function() {
                $(this).closest('.item').removeClass('open');
                $(this).closest('.item').find('.con').attr('aria-expanded', 'false');
            });
        }
    });
    // aslist set
        $('.faqblock .item').each(function() {
            if($(this).find('>.con.aslist').length>0) {
                $(this).find('>a').addClass('withcon');
            }
        });
        $('.faqblock').find('.con.aslist .item a').click(function(e) {
            e.preventDefault();
            if(!$(this).closest('.item').find('>.con.aslist').hasClass('open')) {
                $(this).addClass('open');
                $(this).closest('.item').find('>.con.aslist').addClass('open');
                $(this).closest('.item').find('>.con.aslist').attr('aria-expanded', 'true');
            } else {
                $(this).removeClass('open');
                $(this).closest('.item').find('>.con.aslist').removeClass('open');
                $(this).closest('.item').find('>.con.aslist').attr('aria-expanded', 'false');
            }
        });
}
function _init_history() {
    if($('.btnset-history').length<1) return;
    if($(window).width()<640) {
        $('.btnset-history a').click(function() {
            var num = $(this).index() + 1;
            //console.log( num );
            var topp = $('.history-area'+num).parent().position().top;
                topp += $('.historysidebox').position().top;
                topp += $('.historysidebox').closest('.row').position().top;
                //console.log( topp )
            TweenMax.to($('html,body'), .5, {scrollTop:topp,ease:Expo.easeInOut});
        });
    } else {
        $('.historysidebox .item').hide();
        $('.historysidebox .item').first().fadeIn();
        $('.btnset-history a').first().addClass('selected');
        $('.btnset-history a').click(function() {
            var num = $(this).index() + 1;
            $('.historysidebox .item').hide();
            $('.historysidebox .item').eq(num-1).fadeIn();
            $('.btnset-history a').removeClass('selected');
            $(this).addClass('selected');

        });
    }
}
function _init_btnback() {
    if($('.btn-historyback').length<1) return;
    $('.btn-historyback').click(function(e) {
        e.preventDefault();
        history.back(1);
    });
}
function _init_scroll() {
    $(window).scroll(function() {
        var st = $(document).scrollTop();
        //console.log(st);
        if(st>$(window).height()*.2) {
            if(!$('.header').hasClass('shorten')) {
                $('body').addClass('shorten');
                $('.header').addClass('shorten');
            }
        } else {
            if($('.header').hasClass('shorten')) {
                $('body').removeClass('shorten');
                $('.header').removeClass('shorten');
            }
        }


    });
}
function _init_size() {}
function _init_share() {
    if($('.shareset').length<1) return;
    var theurl = encodeURIComponent(document.location);
    var title = ((_onlang=='zh-tw')?'【TPEx證券櫃檯買賣中心】 ':'TPEx | ')+$('h1').first().text();
    var msg = $('.maincon p').first().text() +' '+ $('.maincon p').eq(1).text();
        if(msg=='') msg = $('[data-name="content"]').text();

    $('.btn-share-fb').click(function() {
        window.open("http://www.facebook.com/sharer/sharer.php?u="+theurl);
    });
    $('.btn-share-line').click(function() {
        window.open('http://line.me/R/msg/text/?'+theurl);
    });
    $('.btn-share-mail').click(function() {
        window.open('mailto:?subject='+title+'&body='+msg+' '+theurl);
    });

    // preset objid
    $('.pdfobj').attr('id', 'pdfobj');
    $('.btn-share-print').click(function(e) {
        e.preventDefault();
        if($('object').length>0) {
            var doc = document.getElementById('pdfobj');
            window.open($('.pdfobj').attr('data'));
            return;
        } else {
            window.print();
        }
    });
}

function _openv(path) {
    window.open(path);
}
function _openpop_register() {
    var b = $('.popup-register').clone();
    $('.container .popup-register').remove();
    $('.popup-register').remove();
    $('body').safeAppend(b);
    $('.popup-register').show();
    $('.popup-register .btn-close').click(function() {
        $('.popup-register').hide();
    });
}
function _openpop_live() {
    var b = $('.popup-live').clone();
    $('.container .popup-live').remove();
    $('.popup-live').remove();
    $('body').safeAppend(b);
    $('.popup-live').show();
    $('.popup-live .btn-close').click(function() {
        $('.popup-live').hide();
    });
}

















/*


     _             _             _      _       
  __| |_  __ _ _ _| |_   _ _ ___| |__ _| |_ ___ 
 / _| ' \/ _` | '_|  _| | '_/ -_) / _` |  _/ -_)
 \__|_||_\__,_|_|  \__| |_| \___|_\__,_|\__\___|
                                                

                         
*/



var _chartcolor = ['#ffca76','#f89432','gold','lightgreen','lightblue','lightorange','gray','purple','pink', '#f89432'];
var _chartcolor2 = [function({value, seriesIndex, w}) {if(value<0) {return '#009A00'} else {return '#ffca76'}}, '#ce2000'];
var _chartcolor_updown = [function({value, seriesIndex, w}) {if(value<0) {return '#178c17'} else {return '#be2901'}}, '#ffca76'];
var _chartstroke = {curve:'straight',width:[2, 2], };
var _chartdatalabel = {enabled:false,tickAmount:5,};
var _chartannotationlabel = '';
var _chartannotationborder = '#333'; //'#89f089';
var _chartxaxis = {type:'datetime',tickAmount:5,};
var _charttooltip = {x:{format:'yyyy/MM/dd HH:mm'},};
var _chartchart = {type:'area',height:$(window).width()*.2,zoom:{enabled:false},toolbar:{show:false},};


var _stryesterdayvalue;
var _strvalue = ((_onlang=='zh-tw')?'成交金額(億)':'Value(NTD 100m)');
var _strindex = ((_onlang=='zh-tw')?'櫃買指數':'TPEx Index');
var _strmore = ((_onlang=='zh-tw')?'查看更多':'More');
var _stropen = ((_onlang=='zh-tw')?'開盤':'Open');
var _stryesterday = ((_onlang=='zh-tw')?'昨收':'Yesterday');
var _strhigh = ((_onlang=='zh-tw')?'最高':'High');
var _strlow = ((_onlang=='zh-tw')?'最低':'Low');
var _strfinal = ((_onlang=='zh-tw')?'成交金額':'Value');
var _strbillion = ((_onlang=='zh-tw')?'億元':'(NTD 100m)');
var _stropenvalue = ((_onlang=='zh-tw')?'開盤價':'Open Value');
var _strnodata = ((_onlang=='zh-tw')?'系統查詢無資料':'No Data Available');
var _strpriceindex = ((_onlang=='zh-tw')?'價格指數：':'Price Index: ');
var _strreturnindex = ((_onlang=='zh-tw')?'收益指數：':'Return Index: ');
var _strbuysalevalue = ((_onlang=='zh-tw')?'買賣斷成交值(億)：':'Buy & Sale Value: ');

function _setchart_bigchart(obj, d, customh) {
    var h = $(window).width()*.22; /*if(customh!=null) h = $(window).width()*customh;*/
    if($(window).width()<641) h = $(window).width()*1.1;
    var _yaxis = [];
        _yaxis.push({
            tickAmount:5,
            title:{
                text:d.series[0].name,
                style:{fontSize:'0'},
            },
            labels:{
                style:{colors:'#ff7418',fontWeight:'bold',fontSize:'12px',},
                formatter:(value) => { return Number(value).toFixed(1); },
                offsetX:-10,
            },
        });
        if(d.series[1]!=undefined) {
            _yaxis.push({
                tickAmount:5,
                opposite:true,
                min:0,
                title:{
                    style:{fontSize:'0'},
                },
                labels:{
                    style:{colors:'#f89432',xxxfontWeight:'bold',fontSize:'12px',},
                    offsetX:-30,
                    formatter:(value) => { return Number(value).toFixed(0); },
                },
            });
        }

        function _gethigh(d) { 
            var tmp = 0;
            for(var n=0; n<d.length; n++) {
                if(Number(d[n])>tmp) {
                    tmp = d[n];
                }
            }
            return tmp;
        }
        _yaxis[0]['max'] = _gethigh(d.series[0].data);
        if(d.series[1].data.length<2) {_yaxis[1]['max'] = 5;} else { _yaxis[1]['max'] = _gethigh(d.series[1].data); }
        //console.log( _gethigh(d.series[0].data), _gethigh(d.series[1].data) )
        if(d.min!=undefined && Number(d.min)!=0) {_yaxis[0]['min'] = Number(d.min);}

    var _stroke = {width:[2,1]};

    var _dailylabel = [];
        for(var t=9; t<14; t++) {
            /*5分鐘一次*/

            /*1分鐘一次*/
            var endtt = 60;  if(t==13) endtt = 30; 
            for(var tt=0; tt<endtt; tt++) {
                var th = String(t); if(th.length==1) th = '0'+t;
                var ttt = tt; if(ttt<10) ttt = '0'+tt;
                _dailylabel.push(th+':'+ttt);
            }
        }
        if(!d.onhistory) {
            if( d.series[0].data.length<_dailylabel.length ) {
                for(var n=d.series[0].data.length; n<_dailylabel.length; n++) {
                    d.series[0].data.push(null);
                    d.series[1].data.push(null);
                }
            }

            //var totalnum = 54; /*5分鐘一次，56少2*/
            var totalnum = 270; /*1分鐘一次，272少2*/
            if( d.series[0].data.length>=totalnum ) {
                //console.log( '這兩個數字比對', d.series[0].data[54], d.series[0].data[55], d.series[0].data[55]==d.series[0].data[54] )
                if( d.series[0].data[totalnum]!=d.series[0].data[totalnum+1] || d.series[1].data[totalnum]!=d.series[1].data[totalnum+1] ) {
                    // 延後收盤
                    //console.log('不一樣');
                    var c1 = d.series[0].data[totalnum];
                    var s1 = d.series[1].data[totalnum];
                    //console.log( c1, s1 );
                    _dailylabel.push('13:30');
                    _dailylabel.push('13:33');
                    var tmpobj = $('#'+obj).parent().parent().find('.updatetime span');
                        if(tmpobj.length==0) tmpobj = $('.subinfo .update span');
                    var str = tmpobj.text();
                    //console.log( str )
                    tmpobj.text( str.substr(0, str.length-5)+'33:00' );
                    //console.log( str.substr(0, str.length-5)+'33:00'  )
                } else {
                    //console.log('一樣');
                    d.series[0].data.pop();
                    d.series[1].data.pop();
                }
            }
            //console.log('>>', d.series[0].data.length, _dailylabel.length )
        }
    
        var _tooltip = {
            hideEmptySeries:false,
            y:{formatter:function(value, { series, seriesIndex, dataPointIndex, w }) {
                        if(value==null) return;
                        return Number(value).toFixed(2);}
                    },
            xxxxcustom:function({ series, seriesIndex, dataPointIndex, w }) {
                const value = series[seriesIndex][dataPointIndex];
                const label = w.globals.labels[dataPointIndex];
                const data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
                const colors = w.globals.colors;
                const serieLabels = w.globals.seriesNames;
                let serieItems = '';
                let serieTitle=  '<div class="apexcharts-tooltip-title">'+data.x+' ('+label+')</div>';
                series.forEach((array, index) => {
                    let serieValue = array[dataPointIndex];
                    let serieLabel = serieLabels[index];
                    let serieColor = colors[index];
                    if (serieValue && serieValue !== 0) {
                        serieItems +=
                            '<div class="apexcharts-tooltip-series-group apexcharts-active" style="order:'+index+';display:flex;">'+
                            '<span class="apexcharts-tooltip-marker" style="background-color: '+serieColor+';"></span>'+
                            '<div class="apexcharts-tooltip-text">'+ 
                            '<div class="apexcharts-tooltip-y-group">' +
                            '<span class="apexcharts-tooltip-text-y-label">' + serieLabel +':</span>'+
                            '<span class="apexcharts-tooltip-text-y-value">'+serieValue+'</span>'+
                            '</div>'+
                            '</div>'+
                            '</div>';
                    }
                });
                return serieTitle + serieItems;
            }
        };
        if(d.history>0) {
            _tooltip = {
                y:{formatter:function(value, { series, seriesIndex, dataPointIndex, w }) {return Number(value).toFixed(2);}},
            };
        }

    var _xaxislabels = {rotate:0,trim:false,style:{fontSize:'14px',},};
        if($(window).width()<1090) {
            _xaxislabels = {rotate:-45,trim:false,style:{fontSize:'11px',},};
        }

    // construct
        var options = {
            series: d.series,
            chart: {type:'line',width:'100%',xxxheight:h,zoom:{enabled:false},toolbar:{show:false},},
            stroke: _stroke,
            colors:['#ff7418','#ffd18e',],
            yaxis: _yaxis,
            xaxis: {
                tickAmount:8,labels:{format:'HH/mm'},
                labels:_xaxislabels,
                axisTicks:{show:false,},
                
                
            },
            tooltip: _tooltip,
            grid:{padding:{left:0, right:-25, top:0, bottom:0 },},
            legend:{offsetY:5,itemMargin:{horizontal:0,},}
        };
        if($(window).width()<640) {
            options.chart = {height:h,zoom:{enabled:false},toolbar:{show:false}};
        }
        if(!d.onhistory) {
            options.labels = _dailylabel;
            options.annotations = {
                yaxis:[{
                    y:d.yesterday,// * 1.01,
                    borderColor:_chartannotationborder,strokeDashArray:4,
                }],
            }
        } else {
            options.labels = d.label;
        }
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
        chart.updateOptions({series:d.series});

}
function _setchart(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
    var _series;
    var _nameAU = "每台錢";
    var _name = (d.key === 'AU') ? _nameAU : _strindex;
        if(d.series==undefined) {
            _series = [{name:_name,type:'line',data:d.index}];
        } else {
            _series = d.series;
        }
        var _dailylabel = [];
        for(var t=9; t<14; t++) {
            var endtt = 12;  if(t==13) endtt = 7;
            for(var tt=0; tt<endtt; tt++) {
                var th = String(t); if(th.length==1) th = '0'+t;
                var ttt = tt*5; if(ttt<10) ttt = '0'+tt*5;
                _dailylabel.push(th+':'+ttt);
            }
        }

    // construct
        var options = {
            series: _series,
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            dataLabels: _chartdatalabel,
            labels: _dailylabel,
            colors: _chartcolor,
            stroke: _chartstroke,
            xaxis: {categories:d.label,tickAmount:5,},
            yaxis: {
                title:{style:{fontSize:0}},
                labels:{style:{colors:'#f89432'},offsetX:-10},
            },
            legend: {offsetY:-10,itemMargin: {horizontal:0,},}
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
        chart.updateOptions({series:_series});
        $('#'+obj).parent().find('.subinfo .update span').text( d.updatetime );
}
function _setchart_subinfo(obj, d, customh) {
    // infodata
        var c = 'red';
        if(d.rise<0) c = 'green';
        $('#'+obj).parent().find('.chartinfo .current').text(_formatNumber(d.indextop));
        $('#'+obj).parent().find('.chartinfo .updown').text(d.rise).addClass(c);
        $('#'+obj).parent().find('.chartinfo .percent').text(d.ratio+'%').addClass(c);
        $('#'+obj).parent().find('.subinfo .update span').text(d.updatetime);
        $('#'+obj).parent().find('.subinfo .value span').text(d.value+'億');
        if(d.value==null) {
            $('#'+obj).parent().find('.subinfo .value').remove();
        }
}
function _setchart_line(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
    // construct
        var options = {
            series: [ {name:'', type:'line', data:d.index} ],
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: {width:[2, 2]},
            colors: _chartcolor2,
            dataLabels: _chartdatalabel,
            labels: d.label,
            xaxis: {type:'datetime',tickAmount:5,},
                grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
}
function _setchart_overbuy(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
    // construct
        var options = {
            series: [
                {name:'買買超(億元)', type:'column', data:d.index1},
                {name:'大盤指數', type:'line', data:d.index2}
            ],
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: {width:[0, 2]},
            colors: _chartcolor_updown,
            dataLabels: _chartdatalabel,
            labels: d.label,
            //xaxis: {type:'datetime',tickAmount:8,},
                grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
}
function _setchart_overbuy_withtext(obj, d, customh) {
    
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
        //console.log( d.series )
        var _yaxis = [];
            _yaxis.push({
                tickAmount:5,
                labels:{
                    style:{xxxcolors:'#f89432',xxxcolors:'#ff7418',xxxfontWeight:'bold',fontSize:'12px',},
                    xxxxformatter:(value) => { return Number(value).toFixed(1); },
                    offsetX:-10,
                },
                title:{
                    text:d.series[0].name,
                    style:{fontSize:'12px'},
                },
            });
        if(d.series[1]!=undefined && d.series.length!=3) {
            _yaxis.push({
                opposite:true, 
                tickAmount:5,
                labels:{
                    style:{xxxcolors:'#f89432',xxxcolors:'#ff7418',xxxfontWeight:'bold',fontSize:'12px',},
                    xxxxformatter:(value) => { return Number(value).toFixed(1); },
                    offsetX:-10,
                },
                title:{
                    text:d.series[1].name,
                    style:{fontSize:'12px'},
                },
            });
        }
    var _stroke = {width:[0,2]};
        if(d.series.length<2) _stroke = {width:[2,2,0,0]};
        if(_onlang!='zh-tw') {
            if(d.series.length==3 || d.series.length==1) _yaxis[0].labels.offsetX = 0;
        }
        

    
    function _gethigh(d) { 
        var tmp = 1;
        for(var n=0; n<d.length; n++) {
            if(Number(d[n])>=tmp) {
                tmp = d[n];
            }
        }
        return tmp;
    }
    function _getlow(d) { 
        var tmp = 1000000000000000;
        for(var n=0; n<d.length; n++) {
            if(Number(d[n])<=tmp) {
                tmp = d[n];
            }
        }
        return tmp;
    }
    if(d.series.length==4) {
        _yaxis[1]['max'] = _gethigh(d.series[1].data);
        _yaxis[1]['min'] = _getlow(d.series[1].data);
    }
    if(d.series.length==3) {
        _yaxis[0]['max'] = _gethigh(d.series[0].data);
        _yaxis[0]['min'] = _getlow(d.series[0].data);
    }
    var _chartcolor_updown = [
                function({value, seriesIndex, w}) {if(value<0) {return '#178c17'} else {return '#be2901'}},
                '#ffca76',
                '#ea510f',
                '#08b931'
            ];
            if(d.series.length==3) {
                _chartcolor_updown = [
                    function({value, seriesIndex, w}) {if(value<0) {return '#178c17'} else {return '#be2901'}},
                    '#ea510f',
                    '#08b931'
                ];
            }



    // construct
        var options = {
            series: d.series,
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: _stroke,
            colors: _chartcolor_updown,

            dataLabels: _chartdatalabel,
            labels: d.label,
            yaxis:_yaxis,
            legend:{show:false,},
            tooltip:{
                enabled:true,
                onDatasetHover: {
                    highlightDataSeries:true,
                },
            },
            xaxis: {
                tickAmount:8,
                axisTicks:{show:false,},
            },
            grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();


        $('.apexcharts-series path').mouseover(function() {
            var __cccc = String($(this).attr('fill')+'!important');
            //console.log( __cccc, $(this).closest('.apexcharts-canvas').find('.apexcharts-tooltip').find('.apexcharts-tooltip-marker').first().attr('class') );
            $(this).closest('.apexcharts-canvas')
                .find('.apexcharts-tooltip')
                .find('.apexcharts-tooltip-marker')
                .first()
                .safeAppend('<span style="display:block; width:100%; height:100%; position:absolute; top:0; left:0; border-radius:.5em; background:'+__cccc+'"></span>');
               
        });
}
function _setchart_overbuy2(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
    // construct
        var options = {
            series: [
                {name:'買買超(億元)', type:'column', data:d.index1},
            ],
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: {width:[0, 2]},
            colors: _chartcolor_updown,
            dataLabels: _chartdatalabel,
            labels: d.label,
            xaxis: {type:'datetime',tickAmount:5,},
                grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
}
function _setchart_bar(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;

        var seriedata = {name:'',type:'column',data:d.index}, ww = [0, 2];
            if(d.asline==true) {
                seriedata = {name:'',type:'line',data:d.index};
                ww = [2];
            }

    // construct
        var options = {
            series: [seriedata],
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: {width:ww},
            colors: _chartcolor2,
            dataLabels: _chartdatalabel,
            yaxis: {tickAmount:5,},
            xaxis: {
                tickAmount:5,labels:{format:'HH/mm'},
                labels:{
                    rotate:0,trim:false,
                    xxxoffsetX:-20,
                    formatter:(value) => { return Number(value).toFixed(2); },
                },
            },
            labels: d.label,
                grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
}
function _setchart_bondmline(obj, d, customh) {
    var h = $(window).width()*.14; /*if(customh!=null) h = $(window).width()*customh;*/
        if($(window).width()<641) h = $(window).width()*.6;
    // construct
        var tmp = [];
        for(var n=0; n<d.name.length; n++) {
            tmp.push({
                name:d.name[n], type:'line', 
                data:d['index'+(n+1)],
            });
        }
        var options = {
            series: tmp,
            chart: {type:'line',xxxxheight:h,width:'100%',zoom:{enabled:false},toolbar:{show:false},},
            stroke: {width:[2,2,2,2,2,2,2,2,2,2,2]},
            colors: ['#ffca76','#ff8c00','#ff0e00','#90ee90','#aed8e6','#8c0000','#808080','#800081','#ffc1cc'],
            dataLabels: _chartdatalabel,
            labels: d.label,
            yaxis: {
                tickAmount:5,labels:{format:'HH/mm'},
                title:{rotate:0,xtext:'%',offsetX:10,},
                labels:{
                    rotate:0,trim:false,
                    offsetX:-15,
                    formatter:(value) => { return Number(value*100).toFixed(1)+'%'; },
                },
            },
            xaxis: {
                tickAmount:8,
                labels:{
                    formatter:(value) => { 
                        var mm = value%12;
                        var yy = parseInt(value/12);
                        var tmp = '';
                            if(yy>0) tmp = yy+_stryear;
                            if(mm>0) {
                                tmp += mm+_strmonth;
                            }
                        return tmp;
                    },
                },
            },
            grid:{padding:{left:0, right:0, top:0, bottom:0 },},
        };
        var chart = new ApexCharts(document.querySelector('#'+obj), options);
        chart.render();
}

function _setchart_pre(obj, d) {
    var b = '';
    b += '<strong>指數：'+d.index+'<span class="change">'+d.change+'</span></strong>';
    b += '<p class="note">資料更新時間：'+d.time+'</p>';
    $('#'+obj).parent().find('h2').next().safePrepend(b);
    var tmp = 'rise'; if(d.change<0) { tmp = 'drop'; }
    $('#'+obj).parent().find('.change').addClass(tmp);
}
function _setchart_pre2(obj, d) {
    var b = '';
    b += '<strong>'+_strpriceindex+d.pindex+'<span class="change">'+d.pchange+'</span></strong>';
    b += '<strong>'+_strreturnindex+d.gindex+'<span class="change">'+d.gchange+'</span></strong>';
    b += '<strong>'+_strbuysalevalue+d.value+'</strong>';
    $('#'+obj).parent().find('h2').next().safePrepend(b);
    var tmp = 'rise'; if(d.change<0) { tmp = 'drop'; }
    $('#'+obj).parent().find('.change').addClass(tmp);
}
function _checkgrouplast(target) {
    var total = target.closest('.group3').find('li').length;
    var n = 0;
    target.closest('.group3').find('li').each(function() {
        $(this).attr('data-order', n);
        n++;
    });
    var on = parseInt(target.closest('li').attr('data-order'));
    if(on==total-1) { return true; } else { return false; }
}
function _presetsidemenu() {
    $('.sidemenu').find('ul>a').addClass('skip').append('skip').css({ display:'block', height:0, width:0, color:'pink', overflow:'hidden' });
    var n = 0;
    $('.sidemenu').find('li').each(function() {
        if($(this).children('a').length>0) { 
            $(this).attr('data-order', n);
            n++;
        }
    });
}
function _whosnext(target) {
    var pobj = target.parent();
    var nobj = pobj.next();
    var n = pobj.index();
    var total = pobj.closest('.group3').find('li').length;

        if( target.attr('href')==undefined && pobj.index()==0 ) {
            //console.log('herer');
            pobj.closest('.onlevel1').find('.megatabset').find('.selected').focus();
        }
        if( pobj.hasClass('level3') ) {
            total = pobj.closest('ul').find('li.level3').length;
            nobj = pobj.next();
        } else if( pobj.hasClass('level4') ) {
            total = pobj.closest('.group3').find('li.level4').length;
            if(n<total) {
                nobj = pobj.next();
            } else {
                nobj = target.closest('.group3').parent().next();
            }
        } else if( pobj.hasClass('level5') ) {
            total = pobj.closest('.group4').find('li.level5').length;
        }
    
    return nobj;
}

var ontab = false;
var onshift = false;
var int_feature = {};
var int_otherlink = {};
function _init_accessbility() {
    
    //return;


    // preset
        $('.accesskey').attr('href', '#');
        $('.accesskey').on('click', function(e) {if(!ontab)e.preventDefault();});
        $('.btn-menu').attr('href', '#');
        _presetsidemenu();



    // keys
        let keys = { end:35, home:36, left:37, up:38, right:39, down:40, delete:46, enter:13, space:32};
        let direction = { 37:-1, 38:-1, 39:1, 40:1};

    // default setting
        $(document).on('keyup', function(e) {
            //ontab = false;
            onshift = false;
        });
        $(document).on('keydown', function(e) {

            var target = $(e.target);
            var pobj = target.parent();
            var which = e.which;
                if(e.shiftKey) onshift = true;


            // ============================================
            // TAB
            // ============================================
                if(!onshift && which==9) {
                    ontab = true;
                    $('body').addClass('accessmode');
                    
                    // 開始即設定
                    if(int_feature!=undefined) {
                        clearInterval(int_feature);
                        clearInterval(int_otherlink);
                    }
                    // 日期物件
                    $('input').attr('readonly', false);
                    $('.daterangepicker').css({visibility:'hidden'});
                    if(String(target.attr('name')).toLowerCase().indexOf('date')>-1 ) {
                        target.attr('readonly', false);
                    }
                    
                    // 0. main menu
                        if(target.hasClass('level1') ) {
                            var alloww = $(window).width() - $('.logo').width()*4;
                            if(target.closest('.onlevel1').position().left > alloww ) {
                                $('.nav.fullh').css({left:-alloww});
                                $('.btn-next').addClass('open');
                            } else {
                                $('.nav.fullh').css({left:0});
                                $('.btn-next').removeClass('open');
                            }

                            // last one
                            if(target.parent().is(':last-of-type') || target.hasClass('btn-next')) {
                                $('.sidemenu').addClass('open');
                                $('.sidemenu').find('.accesskey.access-s').css({background:'transparent', opacity:1});
                            }
                        }
                    
                    // 1. megamenu
                        if(target.closest('.megamenu').length>0) {
                            if(target.hasClass('level3') || target.hasClass('level4') || target.hasClass('level5') ) {}
                            if(pobj.is(':last-of-type') ) {
                                //console.log( '===TAB按鍵', 'ON LEVEL2最後物件' );
                                if(target.hasClass('level3') || target.hasClass('level4') || target.hasClass('level5') || target.parent().hasClass('ad')  ) {
                                    var totalcon = $(target).closest('.megamenu').find('.con').length;
                                    var i = parseInt( $(target).closest('.con').attr('data-order') );
                                        if($(target).hasClass('conlast')) {
                                            i++;
                                            if(i>totalcon) {
                                                // to next nav
                                                // console.log('切換：ON LAST CON, TO NEXT NAV');
                                                target.closest('.onlevel1').find('.megamenu').hide();
                                                target.closest('.onlevel1').find('.megatabset').removeClass('hover');
                                                target.closest('.onlevel1').removeClass('hover');
                                                target.closest('.onlevel1').next().addClass('hover').focus();
                                                target.closest('.onlevel1').next().find('.megamenu').show();
                                                target.closest('.onlevel1').next().find('.megatabset').addClass('hover');
                                                target.closest('.onlevel1').next().find('.megamenu .con').first().find('a').first().focus();
                                            } else {
                                                target.closest('.con').hide();
                                                target.closest('.megamenu').find('.con'+i).show().find('a').first().focus();
                                                target.closest('.megamenu').parent().find('.megatabset .tab').removeClass('selected');
                                                target.closest('.megamenu').parent().find('.megatabset .tab'+i).addClass('selected');
                                                // console.log('這裡2');
                                            }
                                        }
                                        _caltotalgapheight();
                                }
                            }
                        }
                    // 2. megatabset
                        if(target.closest('.megatabset').length>0) {
                            if(target.hasClass('level2') ) {
                                var i = parseInt($(target).index());
                                pobj.parent().find('.con').hide();
                                pobj.parent().find('.con').eq(i).show().find('a').first().focus();
                            }
                        }
                    // 3. sidemenu
                        if(target.closest('.sidemenu').length>0) {
                            target.parent().find('.group').addClass('open');
                            if(target.hasClass('accesskey')) {}
                            var obj = _whosnext(target);
                            if(obj.find('.group3').length>0) {
                                obj.find('.group3').addClass('open');
                            }
                        }
                }


            // ============================================
            // REVERSE TAB
            // ============================================
                if(onshift && which==9) {

                    // 1. megamenu
                        //console.log( '===REVERSE TAB按鍵' );
                        // 0. mainmenu
                        if(target.hasClass('level1') ) {
                            var alloww = $(window).width() - $('.logo').width()*3;
                            if(target.closest('.onlevel1').position().left > alloww ) {
                                $('.nav.fullh').css({left:-alloww});
                                $('.btn-next').addClass('open');
                            } else {
                                $('.nav.fullh').css({left:0});
                                $('.btn-next').removeClass('open');
                            }
                        }

                        var i = target.closest('.con').index();

                        // 1. megamenu ad
                        if( target.index()==0 && target.parent().hasClass('ad')) {
                            target.closest('ul').find('li').last().find('a').focus();
                        }
                        if( target.parent().index()<2 ) {
                            //console.log( 'parentis3 or 2' );
                            target.closest('.onlevel1').find('.megatabset').find('.tab.selected').next().focus();
                        }
                        if( target.attr('href')=='' && target.parent().is('ul') && target.parent().index()==0 ) {
                            target.closest('.onlevel1').find('.megatabset').find('.tab.selected').next().focus();
                        }
                        if(target.hasClass('btn-close')) {
                            target.closest('.onlevel1').find('.megatabset').find('.tab.selected').next().focus();
                        }
                        if(target.hasClass('level2')) {
                            target.closest('.onlevel1').find('.megamenu').hide();
                            target.closest('.onlevel1').removeClass('hover');
                            target.closest('.onlevel1').find('.megatabset').removeClass('hover');
                            $('.overlay').hide();
                        }
                }


            // ============================================
            // ARROW
            // ============================================
                if(which==37 || which==39) {
                    if(ontab) {
                        //console.log( '===TAB按鍵', '左右切換', target );
                        if(which==39) {
                            target.next().focus();
                        }
                        if(which==37) {
                            target.prev().focus();
                        }
                    }
                }
                if(which==38 || which==40) {
                    if(ontab) {
                        //console.log( '===TAB按鍵', '上下切換', target, );
                        if(which==38) {
                            target.prev('a').focus();
                        }
                        if(which==40) {
                            target.next('a').focus();
                        }
                    }
                }

            // ============================================
            // ENTER
            // ============================================
                if(which==13) {
                    //console.log( '===ENTER按鍵', target.attr('class'), target.attr('href') );
                    if(target.attr('href')!='' && target.attr('href')!=undefined) {
                        if(String(target.attr('href')).indexOf('http')>-1) {
                            window.open(target.attr('href'));
                        } else {
                            document.location = target.attr('href');
                        }
                    }
                    if(target.hasClass('level1')) {
                        $('.header .nav li').removeClass('hover');
                        $('.megatabset.hover').removeClass('hover');
                        $('.megamenu').hide();
                        $('.header').addClass('hover');
                        $('.overlay').show();
                        pobj.addClass('hover');
                        pobj.find('.megatabset').addClass('hover');
                        pobj.find('.megatabset .tab').removeClass('selected');
                        pobj.find('.megamenu').show();
                        pobj.find('.megamenu .con').hide();
                        pobj.find('.megamenu .con').first().show();
                        _caltotalgapheight();

                        // getfirst level3 obj
                        var firsta = pobj.find('.megamenu .con').first().find('li').eq(0).find('a');
                            firsta = pobj.find('.megatabset .tab').first();
                            firsta.addClass('selected');
                            firsta.focus();

                        e.preventDefault();
                    }

                    // tab切換
                    if(target.hasClass('level2') || target.hasClass('tab') ) {
                        //console.log( '===TAB按鍵', '選取！', $(target).index() );
                        pobj.addClass('hover');
                        target.parent().find('a').removeClass('selected');
                        target.addClass('selected');
                        target.closest('.onlevel1').find('.megamenu').find('.con').hide();
                        target.closest('.onlevel1').find('.megamenu').find('.con').eq(target.index()).show();
                        //target.closest('.onlevel1').find('.megamenu').find('.con').eq(target.index()).find('li').first().find('a').focus();
                        _caltotalgapheight();
                        e.preventDefault();
                    }
                    if(target.hasClass('level3') || target.hasClass('level4') || target.hasClass('level5') || target.hasClass('gap') ) {
                        //console.log( '===LEVEL 3', '選取！', $(target).index() );
                        e.preventDefault();  
                    }


                    // 日期物件
                    if(String(target.attr('name')).toLowerCase().indexOf('date')>-1 ) {
                        target.attr('readonly', false);
                    }
                    // 手機版物件
                    if(target.hasClass('btn-menu')) {
                        $('.level1').first().focus();
                    }
                    if(target.hasClass('btn-menu') && target.hasClass('open')) {
                        $('.level1').first().focus();
                    }

                }

        });
    $(window).mousedown(function() {
        ontab = false;
        $('body').removeClass('accessmode');
        //$('input').attr('readonly', 'readonly');
        $('.daterangepicker').css({visibility:'visible'});
    });
}






/*
  _      _ _   
 (_)_ _ (_) |_ 
 | | ' \| |  _|
 |_|_||_|_|\__|
               
*/



var _menulink_tw  = '/data/menu/zh-tw/menu.json';
var _menulink_en  = '/data/menu/en-us/menu.json';
var url = document.location.pathname;
var urlsite = document.location.host;
var _onlang = /^en/i.test(document.documentElement.lang)?'en-us':(/jp/i.test(document.documentElement.lang)?'ja-jp':'zh-tw');
$(document).ready(function() {

    _stryesterdayvalue = ((_onlang=='zh-tw')?'昨收':'Yesterday');
    _strvalue = ((_onlang=='zh-tw')?'成交金額(億元)':'Value(NTD 100m)');
    _strindex = ((_onlang=='zh-tw')?'指數':'Index');
    _strmore = ((_onlang=='zh-tw')?'查看更多':'More');
    _stropen = ((_onlang=='zh-tw')?'開盤':'Open');
    _stryesterday = ((_onlang=='zh-tw')?'昨收':'Yesterday');
    _strhigh = ((_onlang=='zh-tw')?'最高':'High');
    _strlow = ((_onlang=='zh-tw')?'最低':'Low');
    _strfinal = ((_onlang=='zh-tw')?'成交金額':'Value');
    _strbillion = ((_onlang=='zh-tw')?'億元':'(NTD 100m)');
    _stropenvalue = ((_onlang=='zh-tw')?'開盤價':'Open Value');
    _strnodata = ((_onlang=='zh-tw')?'系統查詢無資料':'No Data Available');
    _strmonth = ((_onlang=='zh-tw')?'個月':' Month');
    _stryear = ((_onlang=='zh-tw')?'年':' Year ');
    _strpriceindex = ((_onlang=='zh-tw')?'價格指數：':'Price Index: ');
    _strreturnindex = ((_onlang=='zh-tw')?'收益指數：':'Return Index: ');
    _strbuysalevalue = ((_onlang=='zh-tw')?'買賣斷成交值(億)：':'Buy & Sale Value(NTD 100m): ');

    _init_menu();
    _init_form();
    _init_sticky();
    _init_quicktab();
    _init_faq();
    _init_share();
    _init_history();
    _init_btnback();
    _init_size();
    _init_accessbility();


});































































































































