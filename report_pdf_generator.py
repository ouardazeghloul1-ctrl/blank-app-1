# داخل create_pdf_from_content

charts_by_chapter = st.session_state.get("charts_by_chapter", {})
chapter_index = 0
chart_cursor = {}
text_since_chart = 0
first_chapter_processed = False  # ⭐ الحل الجذري

lines = content_text.split("\n")

for raw in lines:
    clean = clean_text(raw)

    if not clean:
        story.append(Spacer(1, 0.8 * cm))
        continue

    # -------- CHAPTER --------
    if clean.startswith("الفصل"):
        # ✅ لا نكسر الصفحة قبل الفصل الأول
        if first_chapter_processed:
            story.append(PageBreak())

        chapter_index += 1
        chart_cursor[chapter_index] = 0
        text_since_chart = 0

        story.append(
            KeepTogether([
                Paragraph(ar(clean), chapter),
                Spacer(1, 0.6 * cm)
            ])
        )

        first_chapter_processed = True
        continue
