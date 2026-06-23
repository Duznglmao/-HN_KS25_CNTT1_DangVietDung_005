from rich.console import Console
from rich.panel import Panel
from tabulate import tabulate

console = Console()


class Booking:
    def __init__(
        self,
        id: str,
        customer_name: str,
        room_number: int,
        room_price: int,
        nights: int,
        service_fee: int,
        discount: int,
    ):
        self.id = id
        self.customer_name = customer_name
        self.room_number = room_number
        self.room_price = room_price
        self.nights = nights
        self.service_fee = service_fee
        self.discount = discount

        self.total_rent = 0
        self.rent_type = ""

        self.calculate_total_rent()
        self.classify_rent()

    def calculate_total_rent(self):
        rent = (self.room_price * self.nights) + self.service_fee - self.discount
        self.total_rent = max(0, rent)

    def classify_rent(self):
        if self.total_rent < 1000000:
            self.rent_type = "Tiết kiệm"
        elif self.total_rent < 3000000:
            self.rent_type = "Tiêu chuẩn"
        elif self.total_rent < 7000000:
            self.rent_type = "Cao cấp"
        else:
            self.rent_type = "VIP"

    def to_list(self):
        return [
            self.id,
            self.customer_name,
            self.room_number,
            self.room_price,
            self.nights,
            self.service_fee,
            self.discount,
            self.total_rent,
            self.rent_type,
        ]


class BookingManager:
    def __init__(self):
        self.bookings = [
            Booking("B001", "Nguyễn Minh Hiển", 301, 250000, 4, 15000, 10000),
            Booking("B002", "Quách Trần Anh", 205, 1500000, 2, 50000, 0),
            Booking("B003", "Vũ Lê Minh Hiếu", 666, 660000, 6, 60000, 6000),
        ]

    @staticmethod
    def validate_id(id, booking_list):
        id = id.strip().upper()
        if not id:
            raise ValueError("Mã đặt phòng không được để trống!")
        if any(booking.id == id for booking in booking_list):
            raise ValueError("Mã đặt phòng không được trùng!")
        return id

    @staticmethod
    def validate_space(text):
        if not text.strip():
            raise ValueError("Họ tên khách hàng không được để trống!")
        return " ".join(text.strip().split())

    @staticmethod
    def validate_room(room):
        if not room.strip():
            raise ValueError("Số phòng không được để trống!")
        if not room.isdigit():
            raise ValueError("Số phòng phải là số nguyên hợp lệ!")
        return int(room)

    @staticmethod
    def validate_number(number, field_name):
        if not number.strip():
            raise ValueError(f"{field_name} không được để trống!")
        if not number.isdigit():
            raise ValueError(f"{field_name} phải là số nguyên hợp lệ!")
        return int(number)

    def find_booking_id(self, id):
        id = id.strip().upper()
        if not id:
            raise ValueError("Mã đặt phòng không được để trống!")
        return next((booking for booking in self.bookings if booking.id == id), None)

    def show_all(self):
        if not self.bookings:
            console.print("[bold red]Danh sách đặt phòng đang rỗng!")
            return

        headers = [
            "Mã đặt phòng",
            "Họ tên khách hàng",
            "Số phòng",
            "Giá/Đêm",
            "Số đêm",
            "Phụ phí",
            "Giảm giá",
            "Tổng tiền",
            "Phân loại",
        ]
        table_data = [booking.to_list() for booking in self.bookings]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    def add_booking(self):
        try:
            new_id = self.validate_id(
                input("Mời nhập vào mã đặt phòng: "), self.bookings
            )
            new_name = self.validate_space(input("Mời nhập vào họ tên khách hàng: "))
            new_room = self.validate_room(input("Mời nhập vào số phòng: "))

            new_room_price = self.validate_number(
                input("Mời nhập vào giá phòng một đêm: "), "Giá phòng"
            )
            if new_room_price < 0:
                raise ValueError("Giá phòng một đêm phải lớn hơn hoặc bằng 0!")

            new_nights = self.validate_number(
                input("Mời nhập vào số đêm thuê: "), "Số đêm thuê"
            )
            if not (1 <= new_nights <= 365):
                raise ValueError("Số đêm thuê phải là số nguyên từ 1 đến 365!")

            new_service_fee = self.validate_number(
                input("Mời nhập vào phụ phí dịch vụ: "), "Phụ phí dịch vụ"
            )
            if new_service_fee < 0:
                raise ValueError("Phụ phí dịch vụ phải lớn hơn hoặc bằng 0!")

            new_discount = self.validate_number(
                input("Mời nhập vào giá trị giảm giá: "), "Giá trị giảm giá"
            )
            if new_discount < 0:
                raise ValueError("Giá trị giảm giá phải lớn hơn hoặc bằng 0!")

            new_booking = Booking(
                new_id,
                new_name,
                new_room,
                new_room_price,
                new_nights,
                new_service_fee,
                new_discount,
            )

            self.bookings.append(new_booking)
            console.print("[bold green]Thêm đặt phòng thành công!")

        except ValueError as e:
            console.print(f"[bold red]Lỗi: {e}")

    def update_booking(self):
        try:
            booking_id = input("Mời nhập vào mã đặt phòng cần cập nhật: ")
            booking = self.find_booking_id(booking_id)

            if booking is None:
                console.print("[bold red]Không tìm thấy đặt phòng cần cập nhật!")
                return

            room_price = self.validate_number(
                input("Mời nhập vào giá phòng mới: "), "Giá phòng"
            )
            if room_price < 0:
                raise ValueError("Giá phòng một đêm phải lớn hơn hoặc bằng 0!")

            nights = self.validate_number(
                input("Mời nhập vào số đêm thuê mới: "), "Số đêm thuê"
            )
            if not (1 <= nights <= 365):
                raise ValueError("Số đêm thuê phải là số nguyên từ 1 đến 365!")

            service_fee = self.validate_number(
                input("Mời nhập vào phụ phí dịch vụ mới: "), "Phụ phí dịch vụ"
            )
            if service_fee < 0:
                raise ValueError("Phụ phí dịch vụ phải lớn hơn hoặc bằng 0!")

            discount = self.validate_number(
                input("Mời nhập vào giá trị giảm giá mới: "), "Giá trị giảm giá"
            )
            if discount < 0:
                raise ValueError("Giá trị giảm giá phải lớn hơn hoặc bằng 0!")

            booking.room_price = room_price
            booking.nights = nights
            booking.service_fee = service_fee
            booking.discount = discount

            booking.calculate_total_rent()
            booking.classify_rent()

            console.print("[bold green]Cập nhật đặt phòng thành công!")

        except ValueError as e:
            console.print(f"[bold red]Lỗi: {e}")

    def delete_booking(self):
        try:
            booking_id = input("Mời nhập vào mã đặt phòng cần xóa: ")
            booking = self.find_booking_id(booking_id)

            if booking is None:
                console.print("[bold red]Không tìm thấy đặt phòng cần xóa!")
                return

            confirm = (
                input(f"Bạn có chắc muốn xóa đặt phòng {booking.id} không? (Y/N): ")
                .strip()
                .upper()
            )

            if confirm == "Y":
                self.bookings.remove(booking)
                console.print("[bold green]Xóa đặt phòng thành công!")
            elif confirm == "N":
                console.print("[bold blue]Đã hủy thao tác xóa!")
            else:
                console.print("[bold red]Lựa chọn không hợp lệ!")

        except ValueError as e:
            console.print(f"[bold red]Lỗi: {e}")

    def search_booking(self):
        console.print("[bold cyan]--- TÌM KIẾM ĐẶT PHÒNG ---")
        keyword = input("Nhập từ khóa tìm kiếm (Tên hoặc Số phòng): ").strip().lower()

        if not keyword:
            console.print("[bold red]Từ khóa không được để trống!")
            return

        results = [
            booking
            for booking in self.bookings
            if keyword in booking.customer_name.lower()
            or keyword in str(booking.room_number)
        ]

        if not results:
            console.print("[bold red]Không tìm thấy đặt phòng phù hợp!")
        else:
            console.print(f"[bold green]Tìm thấy {len(results)} kết quả phù hợp")
            for booking in results:
                console.print(
                    f"[bold yellow]{booking.customer_name} - Phòng {booking.room_number}"
                )

    def run(self):
        while True:
            menu_text = """================ MENU ================
1. Hiển thị danh sách đặt phòng
2. Thêm đặt phòng mới
3. Cập nhật đặt phòng
4. Xóa đặt phòng
5. Tìm kiếm đặt phòng
6. Thoát
====================================="""
            console.print(Panel(menu_text, style="Blue", expand=False))
            choice = input("Nhập lựa chọn của bạn: ").strip()

            match choice:
                case "1":
                    self.show_all()
                case "2":
                    self.add_booking()
                case "3":
                    self.update_booking()
                case "4":
                    self.delete_booking()
                case "5":
                    self.search_booking()
                case "6":
                    console.print(
                        "[bold green]Cảm ơn bạn đã sử dụng hệ thống quản lý đặt phòng khách sạn!"
                    )
                    break
                case _:
                    console.print("[bold red]Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    manager = BookingManager()
    manager.run()
