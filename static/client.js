function makeResizableDiv(div, _minimum_width, _minimum_height)
{
    const element = document.querySelector(div);
    const resizers = element.querySelectorAll('.resizer')

    const minimum_width = _minimum_width;
    const minimum_height = _minimum_height;

    let original_width = 0;
    let original_height = 0;
    let original_x = 0;
    let original_y = 0;
    let original_mouse_x = 0;
    let original_mouse_y = 0;

    for (let i = 0;i < resizers.length; i++)
    {
        const currentResizer = resizers[i];
        currentResizer.addEventListener('mousedown', function(e)
        {
	       e.preventDefault()
	       original_width = parseFloat(getComputedStyle(element, null).getPropertyValue('width').replace('px', ''));
	       original_height = parseFloat(getComputedStyle(element, null).getPropertyValue('height').replace('px', ''));
	       original_x = element.getBoundingClientRect().left;
	       original_y = element.getBoundingClientRect().top;
	       original_mouse_x = e.pageX;
	       original_mouse_y = e.pageY;

	       window.addEventListener('mousemove', resize)
	       window.addEventListener('mouseup', stopResize)
        })
	
    	function resize(e)
        {
            var border_thickness = 5; // TODO: make this somehow grab the border px width.

            var acceptible_x = e.pageX;
            var acceptible_y = e.pageY;

            if(e.pageX < border_thickness)
            {
               acceptible_x = border_thickness;
            }
            else if(e.pageX > document.documentElement.clientWidth - border_thickness)
            {
                acceptible_x = document.documentElement.clientWidth - border_thickness;
            }
            if(e.pageY < border_thickness)
            {
               acceptible_x = border_thickness;
            }
            else if(e.pageY > document.documentElement.clientHeight - border_thickness)
            {
                acceptible_y = document.documentElement.clientHeight - border_thickness;
            }

            var changed_x = (acceptible_x - original_mouse_x);
            var changed_y = (acceptible_y - original_mouse_y);

            if(currentResizer.classList.contains('bottom-right'))
            {
                const width = original_width + changed_x;
                const height = original_height + changed_y;
                if(width > minimum_width)
                {
                    element.style.width = width + 'px';
                }
                if(height > minimum_height)
                {
                    element.style.height = height + 'px';
                }
            }
            else if(currentResizer.classList.contains('bottom-left'))
            {
                const height = original_height + changed_y;
                const width = original_width - changed_x;
                if(width > minimum_width)
                {
                    element.style.width = width + 'px';
                    element.style.left = original_x + changed_x + 'px';
                }
                if(height > minimum_height)
                {
                    element.style.height = height + 'px';
                }
            }
            else if (currentResizer.classList.contains('top-right'))
            {
                const width = original_width + changed_x;
                const height = original_height - changed_y;
                if(width > minimum_width)
                {
                    element.style.width = width + 'px';
                }
                if(height > minimum_height)
                {
                    element.style.height = height + 'px';
                    element.style.top = original_y + changed_y + 'px';
                }
            }
            else
            {
                const width = original_width - changed_x;
                const height = original_height - changed_y;
                if(width > minimum_width)
                {
                    element.style.width = width + 'px';
                    element.style.left = original_x + changed_x + 'px';
                }
                if(height > minimum_height)
                {
                    element.style.height = height + 'px';
                    element.style.top = original_y + changed_y + 'px';
                }
            }
    	}
	
        function stopResize()
        {
            window.removeEventListener('mousemove', resize)
        }
    }
}

/*
const keyEvent2JSON = (e) =>
{
	var keyEvent = {};
	keyEvent.keyCode = e.keyCode;
	/*
	for(var key in e)
	{
		// We can't pass object references.
		if(typeof e[key] === 'object' && e[key] !== null)
		{
			continue;
		}
		keyEvent[key] = e[key];
	}
	*\/
	return JSON.stringify(keyEvent);
}
*/

const writeEvent = (text, to_event) => {
	// <ul> element.
	const parent = document.querySelector(to_event);

	// <li> element appending to the <ul> abovve.
	const el = document.createElement('li');
	el.innerHTML = text;

	var updateScroll = false;

	// Scroll so the newest message is visible, unless client themselves scrolled up. 10 is const IMPORTANT_MAGICAL_SCROLLBAR_CONSTANT = 10; in disguise.
    // It's actually the message padding pixel height.
	if(parent.scrollTop + parent.clientHeight + el.scrollHeight + 10 >= parent.scrollHeight)
	{
		updateScroll = true;
	}

	parent.appendChild(el);

	if(updateScroll)
	{
		parent.scrollTop = parent.scrollHeight;
	}
};

const onFormSubmitted = (e, entity) => {
	e.preventDefault();

    const input = document.querySelector("#" + entity + "_chat");
	const text = input.value;

	if(text == "")
	{
		writeEvent("Your message is empty.", "#" + entity + "_events")
		return;
	}

	if(text.length > 256)
	{
		writeEvent("Your message is too long.", "#" + entity + "_events")
		return;
	}

	input.value = '';

	socket.emit(entity + "_message", {data: text});
};

writeEvent('Welcome to Totally Accurate Political Simulator.', "#npc_events");

const socket = io();

/*
"Connect" is called when socket succesfully connects.
*/
socket.on('connect', function()
{
	socket.emit('connection',
	{
		data: 'User Connected'
	})

	/*
	var form = $('form').on('submit', function(e)
	{
		e.preventDefault()
		let user_name = $( 'input.username' ).val()
		let user_input = $( 'input.message' ).val()

		socket.emit('my event',
		{
			user_name : user_name,
			message : user_input
		})
	$('input.message').val( '' ).focus()
	})
	*/
})

socket.on('npc_message', (json) => {
	writeEvent(json.data, "#npc_events");
});

socket.on('player_message', (json) => {
    writeEvent(json.data, "#player_events");
});

/*
window.addEventListener("keydown", (e) =>
{
	var keyEvent = keyEvent2JSON(e);
	socket.emit('keyDown', keyEvent);
});

window.addEventListener("keyup", (e) =>
{
	var keyEvent = keyEvent2JSON(e);
	socket.emit('keyUp', keyEvent);
});
*/

window.onload = function()
{
	document
		.querySelector('#npc_chat-form')
		.addEventListener('submit', function(e)
            {
                onFormSubmitted(e, "npc")
            });

    document
        .querySelector('#player_chat-form')
        .addEventListener('submit', function(e)
            {
                onFormSubmitted(e, "player")
            });

	makeResizableDiv('#div_npc_chat', 400, 200)
	makeResizableDiv('#div_player_chat', 400, 200)
};
