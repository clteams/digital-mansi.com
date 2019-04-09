function adjustPopover(popover, iframe) {
  var height = iframe.contentWindow.document.body.scrollHeight + 'px',
      popoverContent = $(popover).next('.popover-content');
  iframe.style.height = height;
  popoverContent.css('height', height);
}

window.onload = function () {
    $('.ornament').height($('.jumbotron').height() + $('.sobol').height() + 80);
    audio = new Audio('sable.mp3');
    $('.navbar-brand').click(function () {
          audio.play();
          setTimeout(function(){audio.pause();}, 1700);
    });
    $("route").each(function() {
      var link = $("<a></a>");
      var route_title = "";
      var route_content = "";
      $(this).html(
        "(" + $(this).html().replace(/\.\.\./g, '&hellip;').replace(/,/g, '&#8594;').replace(
          /([^<])\//g, '$1&#8596;'
        ).replace(/&#8594;\s*&hellip;\s*&#8594;/g, '&#10230;') + ")"
      );
      link.attr("role", "button").attr("data-toggle", "popover").attr("data-trigger", "hover");
      link.attr("class", "route-link");
      var i = 0;
      while ($(this).attr("place-" + i)) {
        route_title += $(this).attr("place-" + i);
        if ($(this).attr("place-" + (i + 1))) {
          var rel = "rel-" + i + "-" + (i + 1);
          if (!$(this).attr(rel)) {
            route_title += " &#8594; "
          } else if ($(this).attr(rel) == "varies") {
            route_title += " &#8596; ";
          }
        }
        i ++;
      }
      route_title = route_title;
      var rt_insertion = document.createElement("div");
      rt_insertion.innerHTML = route_title;
      //link.attr("title", route_title);
      //link.attr("data-content", route_content);
      link.html($(this).html());
      $(this).parent().append(link);
      var rc_insertion = document.createElement("div");
      rc_insertion.className = "popover-content-div";
      rc_insertion.innerHTML = route_content;
      if ($(this).attr("story")) {
        var story = document.createElement("div");
        story.innerHTML = $(this).attr("story");
        rc_insertion.appendChild(story);
      }
      else if ($(this).attr("last-place-prefix")) {
        var story = document.createElement("div");
        var story_end = "в ";
        if ($(this).attr("last-place-url")) {
          story_end += '<a href="' + $(this).attr("last-place-url") + '">';
        }
        story_end += $(this).attr("last-place-prefix") + " " + $(this).attr("place-" + (i - 1));
        story_end += '</a>';
        if ($(this).attr("alive") == "y") {
          story.innerHTML = "Проживает " + story_end;
        }
        else if ($(this).attr("gender")) {
          story.innerHTML = "Проживал" + ($(this).attr("gender") == "m" ? "а" : "") + " " + story_end;
        }
        rc_insertion.appendChild(story);
      }
      if ($(this).attr("last-place-frame")) {
       var lpf = document.createElement("div");
       lpf.innerHTML = "<hr>" + $(this).attr("last-place-frame");
       rc_insertion.appendChild(lpf);
      }
      if ($(this).attr("age")) {
        var age = document.createElement("div");
        age.innerHTML = "Возраст: <b>" + $(this).attr("age") + "</b>";
        rc_insertion.appendChild(age);
      }
      link.popover({
        html: true,
        trigger: "manual",
        animation: false,
        title: rt_insertion,
        content: rc_insertion
      }).on('mouseenter', function () {
        var _this = this;
        $(this).popover('show');
        $('.popover').on('mouseleave', function () {
            $(_this).popover('hide');
        });
      }).on('mouseleave', function () {
        var _this = this;
        setTimeout(function () {
          if (!$('.popover:hover').length) {
            $(_this).popover('hide');
          }
        }, 200);
      });
      $(this).remove();
    });
};