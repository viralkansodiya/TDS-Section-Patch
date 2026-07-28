frappe.ui.form.on("Tax Withholding Category", {
    refresh(frm) {
        // Clear india_compliance's query override so the Section field falls back
        // to its static options list (set via Property Setter) instead of calling
        // india_compliance's own search endpoint.
        frm.set_query("tds_section", () => ({}));
    },
});
