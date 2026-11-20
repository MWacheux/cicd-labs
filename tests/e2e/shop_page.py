from playwright.sync_api import Locator, Page, expect


class ShopPage:
    def __init__(self, page: Page):
        self.page = page

    def add(self, product_id: str) -> "ShopPage":
        self.page.get_by_test_id(f"add-{product_id}").click()
        return self

    def apply_coupon(self, code: str) -> "ShopPage":
        self.page.get_by_test_id("coupon").fill(code)
        self.page.get_by_test_id("quote-btn").click()
        return self

    def total(self) -> str:
        expect(self.page.get_by_test_id("summary")).to_be_visible()
        return self.page.get_by_test_id("total").inner_text()

    def order(self) -> Locator:
        self.page.get_by_test_id("order-btn").click()
        confirmation = self.page.get_by_test_id("confirmation")
        expect(confirmation).to_be_visible()
        return confirmation
