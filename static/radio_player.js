
/********************************************************************************************************************
 * client side calls to the server
 ********************************************************************************************************************/

/** select the station list to be displayed in the station list / schedule component */
function show_station_list (zone) {
    $( "#station_schedule_selector" ).load( "/component/live_station_list/" + zone );
}

/** select the on-demand schedule to be displayed in the station list / schedule component */
function show_on_demand_schedule () {
    $( "#station_schedule_selector" ).load( "/component/on_demand_schedule" );
}

/** play a station
  * @param string url the station's URL */
function play_url (url) {
    $.get ("/play/live/" + url);
}

/** stop playing and go to 'standby' */
function play_stop () {
    $.get ("/play/stop");
    $( "#station_schedule_selector" ).load( "/component/blank" );
}


/********************************************************************************************************************
 * graphics code for rendering a BBC logo anf the station widgets
 ********************************************************************************************************************/
/** draw the BBC logo on a canvas
 *  @param string id the ID of the canvas to draw on */
function draw_bbc_logo (id) {
    /* set up to draw on the canvas */
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");

    /* draw BBC text */
    ctx.font = "bold italic 20pt Arial";
    ctx.lineWidth=2;
    ctx.textAlign = "center";
    ctx.textBaseline="middle";
    block_text (ctx, "BBC", canvas.width/2, canvas.height/2, true, 3,
                "#000000", "#FFFFFF", "#FFFFFF");
}

/** draw a station on a canvas
 *  @param string id the ID of the canvas to draw on
 *  @param string name the station name to draw */
function draw_station (id, name) {

    /* set up to draw on the canvas */
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");

    /* draw the circle */
    ctx.strokeStyle="#FF0000";
    ctx.lineWidth=5;
    ctx.beginPath();
    var radius;
    if (canvas.width < canvas.height)
        radius = (canvas.width*45)/100;
    else
        radius = (canvas.height*45)/100;
    ctx.arc (canvas.width/2, canvas.height/2, radius,
             (-45.0 / 180.0) * Math.PI, (225.0 / 180.0) * Math.PI);
    ctx.stroke();

    /* sort out where the text will be plotted */
    var parts = name.split(" ");
    var top_title = "";
    var description = "";
    var description_2 = "";
    var bottom_title = "";
    switch (parts.length)
    {
    default:
      description_2 = " " + parts[5];
    case 5:
      description_2 = parts[4] + description_2;
    case 4:
      description = " " + parts[3];
    case 3:
      description = parts[2] + description;
    case 2:
      bottom_title = parts[1];
    case 1:
      top_title = parts[0];
    case 0:
      break;
    }

    /* plot the text */
    ctx.font = "bold italic 24pt Arial";
    ctx.lineWidth=2;
    ctx.textAlign = "center";
    block_text (ctx, top_title, canvas.width/2, (2*canvas.height)/7, true, 3,
                "#000000", "#FFFFFF", "#FFFFFF");
    ctx.font = "16pt Arial";
    ctx.fillStyle = "#FFFFFF"
    if (description_2.length > 0)
    {
      ctx.fillText(description, canvas.width/2, (5*canvas.height)/10);
      ctx.fillText(description_2, canvas.width/2, (7*canvas.height)/10);
    }
    else
      ctx.fillText(description, canvas.width/2, (6*canvas.height)/10);
    ctx.font = "16pt Arial";
    block_text (ctx, bottom_title, canvas.width/2, (14*canvas.height)/15, false, 3,
                "#FFFFFF", "#000000", "#FF0000");
}

/** draw a text string in block characters with background rectangles
  * ctx - the context to draw with
  * text - the string to draw
  * x,y - text position
  * individual - true to draw individual characters with separators,
  *              false to draw the string in a single block
  * padding - the padding between text and background rectangle, in pixels
  * text_colour - colour for the text
  * rect_fill_colour - colour for the rectangle
  * rect_stroke_colour - colour for the outside of the rectangle */
function block_text (ctx, text, x, y, individual, padding,
                     text_colour, rect_fill_colour, rect_stroke_colour)
{
    /* adjust the start position - all plotting is down from top, left */
    text_width = get_text_width (ctx, text);
    if (individual)
        text_width_padded = text_width + (text.length * padding * 2) + ((text.length -1) * padding);
    else
        text_width_padded = text_width + (padding * 2);
    switch (ctx.textAlign)
    {
    case "start":
    case "left":
        break;
    case "end":
    case "right":
        x -= text_width_padded;
        break;
    default:
        x -= text_width_padded / 2;
        break;
    }
    text_height = get_text_height (ctx, text);
    switch (ctx.textBaseline)
    {
    case "top":
    case "hanging":
        break;
    case "bottom":
    case "alphabetic":
        y -= text_height;
        break;
    default:
        y -= text_height / 2;
        break;
    }
    var stored_text_align = ctx.textAlign;
    var stored_text_baseline = ctx.textBaseline;
    ctx.textAlign = "left";
    ctx.textBaseline = "top";

    if (individual)
    {
        /* plot the text, character by character */
        var stored_fill_style = ctx.fillStyle;
        var stored_stroke_style = ctx.strokeStyle;
        var count;
        for (count=0; count<text.length; count++)
        {
            var c = text.charAt (count);
            var c_width = get_text_width (ctx, c);
            ctx.fillStyle = rect_fill_colour;
            ctx.strokeStyle = rect_fill_colour;
            round_rect (ctx, x, y, c_width + (padding * 2), text_height + (padding * 2), 5, true, false);
            ctx.fillStyle = text_colour;
            ctx.fillText(c, x + padding, y + padding);
            x += c_width + padding * 3;
        }
    }
    else
    {
        ctx.fillStyle = rect_fill_colour;
        ctx.strokeStyle = rect_stroke_colour;
        round_rect (ctx, x, y, text_width + (padding * 2), text_height + (padding * 2), 5, true, true);
        ctx.fillStyle = text_colour;
        ctx.fillText(text, x + padding, y + padding);
    }

    /* restore context settings */
    ctx.strokeStyle = stored_stroke_style;
    ctx.fillStyle = stored_fill_style;
    ctx.textAlign = stored_text_align;
    ctx.textBaseline = stored_text_baseline;
}

/**
 * Draws a rounded rectangle using the current state of the canvas.
 * If you omit the last three params, it will draw a rectangle
 * outline with a 5 pixel border radius
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width The width of the rectangle
 * @param {Number} height The height of the rectangle
 * @param {Number} [radius = 5] The corner radius; It can also be an object
 *                 to specify different radii for corners
 * @param {Number} [radius.tl = 0] Top left
 * @param {Number} [radius.tr = 0] Top right
 * @param {Number} [radius.br = 0] Bottom right
 * @param {Number} [radius.bl = 0] Bottom left
 * @param {Boolean} [fill = false] Whether to fill the rectangle.
 * @param {Boolean} [stroke = true] Whether to stroke the rectangle. */
function round_rect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke == 'undefined') {
        stroke = true;
    }
    if (typeof radius === 'undefined') {
        radius = 5;
    }
    if (typeof radius === 'number') {
        radius = {tl: radius, tr: radius, br: radius, bl: radius};
    } else {
        var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
        for (var side in defaultRadius) {
            radius[side] = radius[side] || defaultRadius[side];
        }
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
        ctx.fill();
    }
    if (stroke) {
        ctx.stroke();
    }
}

/**
* Measures text width
* @param  string text   The text to measure
* @param  ctx           The canvas drawing context
* @return The width of the text */
function get_text_width (ctx, text)
{
    var metrics = ctx.measureText (text)
    return metrics.width;
}

/**
* Measures text height by creating a DIV in the document and adding the relevant text to it.
* Then checking the .offsetHeight. Because adding elements to the DOM is not particularly
* efficient in animations (particularly) it caches the measured text width/height.
* @param  ctx           The canvas drawing context
* @param  string text   The text to measure
* @return The height of the text */
function get_text_height(ctx, text)
{
    // This global variable is used to cache repeated calls with the same arguments
    var str = text + ':' + ctx.font;
    if (typeof(__measuretext_cache__) == 'object' && __measuretext_cache__[str]) {
        return __measuretext_cache__[str];
    }

    font_parts = ctx.font.split (" ");
    var div = document.createElement('DIV');
        div.innerHTML = text;
        div.style.position = 'absolute';
        div.style.top = '-100px';
        div.style.left = '-100px';
        div.style.fontFamily = font_parts [font_parts.length -1];
        div.style.fontWeight = ctx.font.indexOf ("bold") == -1 ? 'normal' : 'bold';
        div.style.fontSize = font_parts [font_parts.length -2];
    document.body.appendChild(div);

    var height = div.offsetHeight;

    document.body.removeChild(div);

    // Add the height to the cache as adding DOM elements is costly and can cause slow downs
    if (typeof(__measuretext_cache__) != 'object') {
        __measuretext_cache__ = [];
    }
    __measuretext_cache__[str] = height;

    return height;
}
