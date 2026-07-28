import json

import frappe

from tds_section_patch.constants import NEW_TDS_SECTIONS, OLD_TDS_SECTIONS


def get_all_tds_section_options():
    options = [{"value": section, "label": section, "description": ""} for section in OLD_TDS_SECTIONS]
    options += [
        {
            "value": row["section_name"],
            "label": row["section_name"],
            "description": row.get("description", ""),
        }
        for row in NEW_TDS_SECTIONS
    ]

    seen = set()
    deduped = []
    for row in sorted(options, key=lambda d: d["value"]):
        if row["value"] in seen:
            continue
        seen.add(row["value"])
        deduped.append(row)

    return deduped


def setup_tds_section_field():
    """Widen the existing tds_section field's options to the full latest section list."""
    filters = {
        "doc_type": "Tax Withholding Category",
        "field_name": "tds_section",
        "property": "options",
    }
    value = json.dumps(get_all_tds_section_options())

    name = frappe.db.exists("Property Setter", filters)
    if name:
        doc = frappe.get_doc("Property Setter", name)
        doc.value = value
        doc.save()
    else:
        frappe.get_doc(
            {
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "property_type": "Text",
                **filters,
                "value": value,
            }
        ).insert(ignore_permissions=True)

    frappe.clear_cache(doctype="Tax Withholding Category")
    print("tds_section options updated with latest TDS sections")
