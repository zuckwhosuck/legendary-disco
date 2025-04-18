document.addEventListener("DOMContentLoaded", () => {
    const ball = document.querySelector(".ball");
  
    // Ensure the ball exists
    if (!ball) {
        console.error("Element '.ball' not found!");
        return;
    }
  
    gsap.set(ball, { xPercent: -50, yPercent: -50 });
  
    let xTo = gsap.quickTo(ball, "x", { duration: 0.2, ease: "power3" }),
        yTo = gsap.quickTo(ball, "y", { duration: 0.2, ease: "power3" });
  
    window.addEventListener("mousemove", e => {
        xTo(e.clientX);
        yTo(e.clientY);
    });
  });
  