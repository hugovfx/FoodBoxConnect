document.addEventListener("mousemove", (event) => {
    const bubbles = document.querySelectorAll(".bubble");

    bubbles.forEach((bubble) => {
        const bubbleRect = bubble.getBoundingClientRect();
        const bubbleX = bubbleRect.left + bubbleRect.width / 2;
        const bubbleY = bubbleRect.top + bubbleRect.height / 2;

        const dx = event.clientX - bubbleX;
        const dy = event.clientY - bubbleY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
            const angle = Math.atan2(dy, dx);
            const moveX = -Math.cos(angle) * 20; // Movemos en dirección opuesta
            const moveY = -Math.sin(angle) * 20; // Movemos en dirección opuesta

            bubble.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.2)`;
        } else {
            bubble.style.transform = "scale(1)";
        }
    });
});

window.addEventListener("scroll", function () {
    const navbar = document.getElementById("navbar");
    if (window.scrollY > 20) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});