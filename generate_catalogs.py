"""
PDF Catalog Generator for Tech Fest (Face Paint & Mehendi)
Generates high-resolution, print-ready PDFs with 4 images per page (2x2 grid),
each displaying the Design ID and Price.
"""

import os
import json
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# ---------------------------------------------------------
# Font Setup
# ---------------------------------------------------------
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
    FONT_NORMAL = 'Arial'
    FONT_BOLD = 'Arial-Bold'
except Exception as e:
    print(f"Warning loading system Arial font: {e}, falling back to Helvetica")
    FONT_NORMAL = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'


# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
def load_gallery_and_prices():
    # Load prices
    with open('prices.json', 'r', encoding='utf-8') as f:
        prices_data = json.load(f)

    # Load gallery images from gallery-data.js
    with open('gallery-data.js', 'r', encoding='utf-8') as f:
        js_text = f.read()

    json_str = js_text.split('window.GALLERY_IMAGES =')[1].split(';')[0].strip()
    gallery_data = json.loads(json_str)

    return gallery_data, prices_data


# ---------------------------------------------------------
# Render Helpers
# ---------------------------------------------------------
def draw_rounded_rect(c, x, y, width, height, radius, fill_color=None, stroke_color=None, stroke_width=1):
    c.saveState()
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    else:
        c.setLineWidth(0)
    
    if fill_color:
        c.setFillColor(fill_color)
    
    c.roundRect(x, y, width, height, radius, stroke=1 if stroke_color else 0, fill=1 if fill_color else 0)
    c.restoreState()


def generate_catalog_pdf(output_filename, items, category_title, theme_color_hex, badge_bg_hex, subtitle="Official Design & Price Menu"):
    """
    items: list of dicts: {'id': 1, 'price': 50, 'image_path': 'path/to/img.jpeg'}
    """
    c = canvas.Canvas(output_filename, pagesize=A4)
    page_w, page_h = A4  # 595.28 x 841.89

    theme_color = HexColor(theme_color_hex)
    badge_color = HexColor(badge_bg_hex)
    card_bg = HexColor("#FFFFFF")
    card_border = HexColor("#E2E8F0")
    header_bar_bg = HexColor("#F8FAFC")
    id_pill_bg = HexColor("#0F172A")       # Dark sleek slate
    id_pill_text = HexColor("#FFFFFF")
    text_muted = HexColor("#64748B")
    page_bg = HexColor("#F1F5F9")
    img_box_bg = HexColor("#FAFAFA")
    img_border = HexColor("#ECEFF1")

    # Layout dimensions
    margin_x = 28
    header_top = 818
    header_bottom = 785
    footer_y = 16
    grid_top = 775
    grid_bottom = 34

    usable_w = page_w - (margin_x * 2)  # ~539.28
    usable_h = grid_top - grid_bottom   # ~741

    col_gap = 14
    row_gap = 14

    card_w = (usable_w - col_gap) / 2   # ~262.6 pt
    card_h = (usable_h - row_gap) / 2   # ~363.5 pt

    # Chunk into 4 per page
    pages = [items[i:i + 4] for i in range(0, len(items), 4)]
    total_pages = len(pages)

    print(f"Generating {output_filename}: {len(items)} items across {total_pages} pages...")

    for page_idx, page_items in enumerate(pages):
        page_num = page_idx + 1

        # 1. Subtle soft page background
        c.setFillColor(page_bg)
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # 2. Header Area
        # Left: Main Category Title
        c.setFont(FONT_BOLD, 15)
        c.setFillColor(theme_color)
        c.drawString(margin_x, header_top - 4, category_title.upper())

        # Subtitle
        c.setFont(FONT_NORMAL, 8.5)
        c.setFillColor(text_muted)
        c.drawString(margin_x, header_top - 16, subtitle)

        # Right: Page count badge
        page_str = f"Page {page_num} of {total_pages}"
        c.setFont(FONT_BOLD, 9)
        c.setFillColor(theme_color)
        c.drawRightString(page_w - margin_x, header_top - 12, page_str)

        # Header accent rule
        c.setStrokeColor(theme_color)
        c.setLineWidth(1.8)
        c.line(margin_x, header_bottom, page_w - margin_x, header_bottom)

        # 3. Footer Area
        footer_text = "Tech Fest • Quote the Design ID at the booking desk • Instant application"
        c.setFont(FONT_NORMAL, 8)
        c.setFillColor(text_muted)
        c.drawCentredString(page_w / 2.0, footer_y, footer_text)

        # 4. Render 2x2 Grid of Cards
        for idx_in_page, item in enumerate(page_items):
            # col: 0 (left) or 1 (right)
            col = idx_in_page % 2
            # row: 0 (top) or 1 (bottom)
            row = idx_in_page // 2

            card_x = margin_x + col * (card_w + col_gap)
            card_y = grid_bottom + (1 - row) * (card_h + row_gap)

            # Draw card container
            draw_rounded_rect(c, card_x, card_y, card_w, card_h, radius=7, fill_color=card_bg, stroke_color=card_border, stroke_width=1)

            # Card Header Bar (Height: 34 pt)
            bar_h = 32
            bar_y = card_y + card_h - bar_h
            draw_rounded_rect(c, card_x, bar_y, card_w, bar_h, radius=7, fill_color=header_bar_bg, stroke_color=None)
            # Re-fill lower part of the rounded rect so bottom corners of the header are flat
            c.setFillColor(header_bar_bg)
            c.rect(card_x, bar_y, card_w, 10, fill=1, stroke=0)
            c.setStrokeColor(HexColor("#E2E8F0"))
            c.setLineWidth(0.8)
            c.line(card_x, bar_y, card_x + card_w, bar_y)

            # ID Pill on the left
            id_text = f"ID #{item['id']}"
            c.setFont(FONT_BOLD, 10)
            id_txt_w = pdfmetrics.stringWidth(id_text, FONT_BOLD, 10)
            id_pill_w = id_txt_w + 14
            id_pill_h = 20
            id_pill_x = card_x + 8
            id_pill_y = bar_y + (bar_h - id_pill_h) / 2

            draw_rounded_rect(c, id_pill_x, id_pill_y, id_pill_w, id_pill_h, radius=4, fill_color=id_pill_bg, stroke_color=None)
            c.setFont(FONT_BOLD, 10)
            c.setFillColor(id_pill_text)
            c.drawString(id_pill_x + 7, id_pill_y + 5, id_text)

            # Price Pill on the right
            price_val = item['price']
            if price_val is not None:
                price_text = f"₹ {price_val}"
                cur_badge_color = badge_color
            else:
                price_text = "Custom"
                cur_badge_color = HexColor("#64748B")

            c.setFont(FONT_BOLD, 11)
            price_txt_w = pdfmetrics.stringWidth(price_text, FONT_BOLD, 11)
            price_pill_w = price_txt_w + 14
            price_pill_h = 20
            price_pill_x = card_x + card_w - 8 - price_pill_w
            price_pill_y = bar_y + (bar_h - price_pill_h) / 2

            draw_rounded_rect(c, price_pill_x, price_pill_y, price_pill_w, price_pill_h, radius=4, fill_color=cur_badge_color, stroke_color=None)
            c.setFont(FONT_BOLD, 11)
            c.setFillColor(HexColor("#FFFFFF"))
            c.drawString(price_pill_x + 7, price_pill_y + 5, price_text)

            # Image Box Area
            box_padding = 8
            img_box_x = card_x + box_padding
            img_box_y = card_y + box_padding
            img_box_w = card_w - (box_padding * 2)
            img_box_h = card_h - bar_h - (box_padding * 2)

            # Image backdrop
            draw_rounded_rect(c, img_box_x, img_box_y, img_box_w, img_box_h, radius=5, fill_color=img_box_bg, stroke_color=img_border, stroke_width=0.6)

            # Load and draw image
            img_path = item['image_path']
            if os.path.exists(img_path):
                try:
                    with Image.open(img_path) as pil_img:
                        pil_img = ImageOps.exif_transpose(pil_img)
                        orig_w, orig_h = pil_img.size

                    # Calculate aspect fit inside image box with 4pt inner margin
                    inner_margin = 4
                    fit_w = img_box_w - (inner_margin * 2)
                    fit_h = img_box_h - (inner_margin * 2)

                    scale = min(fit_w / orig_w, fit_h / orig_h)
                    render_w = orig_w * scale
                    render_h = orig_h * scale

                    render_x = img_box_x + inner_margin + (fit_w - render_w) / 2.0
                    render_y = img_box_y + inner_margin + (fit_h - render_h) / 2.0

                    c.drawImage(img_path, render_x, render_y, width=render_w, height=render_h, preserveAspectRatio=True)
                except Exception as img_err:
                    print(f"Error drawing image {img_path}: {img_err}")
                    c.setFont(FONT_NORMAL, 9)
                    c.setFillColor(text_muted)
                    c.drawCentredString(img_box_x + img_box_w / 2, img_box_y + img_box_h / 2, "Image Unavailable")
            else:
                c.setFont(FONT_NORMAL, 9)
                c.setFillColor(text_muted)
                c.drawCentredString(img_box_x + img_box_w / 2, img_box_y + img_box_h / 2, "File Not Found")

        c.showPage()

    c.save()
    print(f"Successfully generated: {output_filename}")


def main():
    gallery_data, prices_data = load_gallery_and_prices()

    # Build Face Paint items
    fp_files = gallery_data.get('facePaint', [])
    fp_prices = prices_data.get('facePaint', {})
    face_paint_items = []
    for idx, fname in enumerate(fp_files):
        design_id = idx + 1
        key = f"f{design_id}"
        price = fp_prices.get(key)
        img_path = os.path.join('face paint', fname)
        face_paint_items.append({
            'id': design_id,
            'price': price,
            'image_path': img_path
        })

    # Build Mehendi items
    m_files = gallery_data.get('mehendi', [])
    m_prices = prices_data.get('mehendi', {})
    mehendi_items = []
    for idx, fname in enumerate(m_files):
        design_id = idx + 1
        key = f"m{design_id}"
        price = m_prices.get(key)
        img_path = os.path.join('mehendi', fname)
        mehendi_items.append({
            'id': design_id,
            'price': price,
            'image_path': img_path
        })

    # Styling themes
    # Face paint: Vibrant Coral Orange
    FP_THEME = "#EA580C"   # Rich Orange
    FP_BADGE = "#FF5722"   # Bright Fest Coral

    # Mehendi: Rich Warm Henna Amber / Brown
    M_THEME = "#9A3412"    # Warm Henna Rust
    M_BADGE = "#D97706"    # Warm Amber Gold

    print(f"Total Face Paint designs: {len(face_paint_items)}")
    print(f"Total Mehendi designs: {len(mehendi_items)}")

    # -------------------------------------------------------------
    # 1. Complete Catalogs (1 PDF each, 2 PDFs total)
    # -------------------------------------------------------------
    generate_catalog_pdf(
        output_filename="Face_Paint_Catalog.pdf",
        items=face_paint_items,
        category_title="Tech Fest • Face Paint Catalog",
        theme_color_hex=FP_THEME,
        badge_bg_hex=FP_BADGE,
        subtitle="Festival Face Art & Creative Designs • 4 per page"
    )

    generate_catalog_pdf(
        output_filename="Mehendi_Catalog.pdf",
        items=mehendi_items,
        category_title="Tech Fest • Mehendi Catalog",
        theme_color_hex=M_THEME,
        badge_bg_hex=M_BADGE,
        subtitle="Traditional & Modern Henna Art • 4 per page"
    )

    # -------------------------------------------------------------
    # 2. Split Catalogs (2 PDFs for Face Paint, 2 PDFs for Mehendi)
    #    In case "2 pdf for each mehendi and face paint" meant 2 PDFs each!
    # -------------------------------------------------------------
    # Face Paint
    fp_mid = (len(face_paint_items) + 1) // 2
    generate_catalog_pdf(
        output_filename="Face_Paint_Catalog_Part_1.pdf",
        items=face_paint_items[:fp_mid],
        category_title=f"Face Paint Catalog — Part 1 (Designs #1 - #{fp_mid})",
        theme_color_hex=FP_THEME,
        badge_bg_hex=FP_BADGE,
        subtitle="Tech Fest 2026 • Part 1 of 2"
    )

    generate_catalog_pdf(
        output_filename="Face_Paint_Catalog_Part_2.pdf",
        items=face_paint_items[fp_mid:],
        category_title=f"Face Paint Catalog — Part 2 (Designs #{fp_mid + 1} - #{len(face_paint_items)})",
        theme_color_hex=FP_THEME,
        badge_bg_hex=FP_BADGE,
        subtitle="Tech Fest 2026 • Part 2 of 2"
    )

    # Mehendi
    m_mid = (len(mehendi_items) + 1) // 2
    generate_catalog_pdf(
        output_filename="Mehendi_Catalog_Part_1.pdf",
        items=mehendi_items[:m_mid],
        category_title=f"Mehendi Catalog — Part 1 (Designs #1 - #{m_mid})",
        theme_color_hex=M_THEME,
        badge_bg_hex=M_BADGE,
        subtitle="Tech Fest 2026 • Part 1 of 2"
    )

    generate_catalog_pdf(
        output_filename="Mehendi_Catalog_Part_2.pdf",
        items=mehendi_items[m_mid:],
        category_title=f"Mehendi Catalog — Part 2 (Designs #{m_mid + 1} - #{len(mehendi_items)})",
        theme_color_hex=M_THEME,
        badge_bg_hex=M_BADGE,
        subtitle="Tech Fest 2026 • Part 2 of 2"
    )

    print("\nAll PDFs generated successfully!")


if __name__ == '__main__':
    main()
