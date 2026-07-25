// ===== Draw measuring-tape ticks on every .ruler =====
document.querySelectorAll(".ruler__ticks").forEach(function (g) {
  const ns = "http://www.w3.org/2000/svg";
  for (let x = 0; x <= 400; x += 8) {
    const tall = x % 40 === 0;
    const line = document.createElementNS(ns, "line");
    line.setAttribute("x1", x);
    line.setAttribute("x2", x);
    line.setAttribute("y1", tall ? 2 : 5);
    line.setAttribute("y2", tall ? 14 : 11);
    line.setAttribute("stroke", "rgba(184,147,91,0.55)"); // brass
    line.setAttribute("stroke-width", tall ? 1.2 : 0.7);
    g.appendChild(line);
  }
});

// PDF filename, injected by the Django template (card/views.py) so it
// always matches whatever the admin has set for the company/person name.
const PDF_FILENAME = (function () {
  const el = document.getElementById("pdf-filename");
  if (!el) return "Business-Card";
  try {
    return JSON.parse(el.textContent) || "Business-Card";
  } catch (err) {
    console.error("Could not read PDF filename:", err);
    return "Business-Card";
  }
})();

// ===== Download Card (PDF) =====
// Renders the hidden #printCard template (a proper business-card layout,
// 1050x600px = 3.5in x 2in at 300dpi) to an image, then embeds that image
// in a real PDF sized to match a physical business card.
(function () {
  const btn = document.getElementById("downloadCard");
  const label = document.getElementById("downloadCardLabel");
  if (!btn) return;

  btn.addEventListener("click", async function () {
    const node = document.getElementById("printCard");
    if (!node || typeof html2canvas === "undefined" || !window.jspdf) {
      alert(
        "The PDF generator did not load. Check your connection and try again.",
      );
      return;
    }

    const originalLabel = label.textContent;
    btn.disabled = true;
    label.textContent = "Preparing…";

    try {
      const canvas = await html2canvas(node, {
        scale: 3,
        backgroundColor: null,
        useCORS: true,
      });
      const imgData = canvas.toDataURL("image/png");

      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF({
        orientation: "landscape",
        unit: "in",
        format: [3.5, 2],
      });
      pdf.addImage(imgData, "PNG", 0, 0, 3.5, 2);
      pdf.save(PDF_FILENAME + ".pdf");
    } catch (err) {
      console.error("Could not generate PDF:", err);
      alert("Could not generate the PDF. Please try again.");
    } finally {
      btn.disabled = false;
      label.textContent = originalLabel;
    }
  });
})();
