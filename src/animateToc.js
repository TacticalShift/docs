
const debounce = (fn) => {
	let frame;
	return (...params) => {
		if (frame) cancelAnimationFrame(frame);
		frame = requestAnimationFrame(()=>{
			fn(...params)
		})
	}
}

const storeScroll = () => {
	const toc = document.getElementsByClassName("toc")[0]
	if (toc == null) return 
	
	if (window.scrollY > 200) {
		toc.classList.add("toc_fixed")
	} else {
		toc.classList.remove("toc_fixed")
	}
}

document.addEventListener("scroll", debounce(storeScroll))
storeScroll()