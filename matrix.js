// NOTE: This file is a copy. The active version is at:
// enrollment/static/enrollment/js/matrix.js
// Please make changes there.


const canvas = document.getElementById("canvas")
const ctx = canvas.getContext('2d')

let cw = window.innerWidth
let ch = window.innerHeight

canvas.width = cw
canvas.height = ch

let particles = []
const particleCount = Math.floor((cw * ch) / 8000)

for (let i = 0; i < particleCount; i++) {
	const angle = Math.random() * Math.PI * 2
	const speed = 0.5 + Math.random() * 2
	particles[i] = {
		x: Math.random() * cw,
		y: Math.random() * ch,
		vx: Math.cos(angle) * speed,
		vy: Math.sin(angle) * speed,
		size: 1.5 + Math.random() * 2.5,
		opacity: 0.3 + Math.random() * 0.5,
		trail: 3 + Math.floor(Math.random() * 6)
	}
}

function draw() {
	ctx.fillStyle = "rgba(3, 7, 18, 0.12)"
	ctx.fillRect(0, 0, cw, ch)

	for (let i = 0; i < particles.length; i++) {
		const p = particles[i]

		for (let j = 0; j < p.trail; j++) {
			const tx = p.x - j * p.vx * 1.5
			const ty = p.y - j * p.vy * 1.5
			const alpha = p.opacity * (1 - j / p.trail) * 0.6

			if (j === 0) {
				ctx.fillStyle = `rgba(180, 255, 180, ${p.opacity * 0.9})`
			} else if (j < 3) {
				ctx.fillStyle = `rgba(0, 255, 65, ${alpha})`
			} else {
				ctx.fillStyle = `rgba(0, 200, 50, ${alpha * 0.5})`
			}

			ctx.beginPath()
			ctx.arc(tx, ty, p.size * (1 - j * 0.08), 0, Math.PI * 2)
			ctx.fill()
		}

		p.x += p.vx
		p.y += p.vy

		if (p.x < 0 || p.x > cw) {
			p.vx *= -1
			p.x = Math.max(2, Math.min(cw - 2, p.x))
		}
		if (p.y < 0 || p.y > ch) {
			p.vy *= -1
			p.y = Math.max(2, Math.min(ch - 2, p.y))
		}
	}

	requestAnimationFrame(draw)
}

draw()

window.addEventListener("resize", () => {
	cw = window.innerWidth
	ch = window.innerHeight
	canvas.width = cw
	canvas.height = ch
})