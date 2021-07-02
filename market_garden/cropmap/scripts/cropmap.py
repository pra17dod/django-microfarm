# manipulation
PRECISION = float(0.1)
ROUND_TO = 1


class Cropmap:
    """
    Cropmap creates a instance of the user-defined parameters required to
    calculate best parameters in order to make optimum use of space.
    """

    def __init__(
        self,
        length: float,
        width: float,
        path_width: float,
        path_width_btw_sections: float,
        min_bed_length: float,
        max_bed_length: float,
        min_bed_per_section: int,
        max_bed_per_section: int,
        bed_width: float,
        compost_height_of_bed: float,
        compost_height_of_path: float,
    ):
        """
        Constructs a new Cropmap of user-defined parameters.
        """

        self.length = float(length)
        self.width = float(width)
        self.path_width = float(path_width)
        self.path_width_btw_sections = float(path_width_btw_sections)
        self.min_bed_length = float(min_bed_length)
        self.max_bed_length = float(max_bed_length)
        self.min_bed_per_section = int(min_bed_per_section)
        self.max_bed_per_section = int(max_bed_per_section)
        self.bed_width = float(bed_width)
        self.compost_height_of_bed = float(compost_height_of_bed)
        self.compost_height_of_path = float(compost_height_of_path)

    def arrangement(self, bed_along_side: float, bed_along_side_name: str) -> list:
        """
        Returns list containing best bed-length, side along which beds are
        to be made and number of beds along that side.

        param:  bed_along_side -> measure the side along
                bed_along_side_name -> name of the side.

        returns: list containing bed_length, bed_along_side and bed_along_side_name.
        """

        if bed_along_side_name == "length":
            otherside = self.width
        else:
            otherside = self.length
        lis = []
        bed_len = self.min_bed_length
        while bed_len <= bed_along_side and bed_len <= self.max_bed_length:
            num_of_bed_along_side = int(bed_along_side / bed_len)
            len_of_section = round(
                (
                    num_of_bed_along_side * bed_len
                    + (num_of_bed_along_side - 1) * (self.path_width_btw_sections)
                ),
                ROUND_TO,
            )

            if len_of_section <= bed_along_side:
                difference = bed_along_side - len_of_section
                if difference >= 0:
                    lis.append(
                        [
                            round(difference, 1),
                            round(bed_len, ROUND_TO),
                            bed_along_side_name,
                            num_of_bed_along_side,
                        ]
                    )
            bed_len = round(bed_len + PRECISION, ROUND_TO)

        # arrangement with min diff i.e., free space to maximize bed length
        lis.sort(key=lambda x: x[0])
        if lis:
            lis = lis[0][1:]  # dropping difference value
        return lis

    def num_of_section(
        self,
        bed_length: float,
        bed_along_side_name: str,
        num_of_bed_along_side: float,
        min_sections: int,
    ) -> tuple:
        """
        Calculates the number of sections using parameters calculated by
        function `arrangement`.

        params: Cropmap parameters calculated by the function `arrangement` and min_sections.

        returns: A tuple of number of bed along otherside, bed per section and
                 total number of sections.
        """

        if bed_along_side_name == "length":
            bed_along_side = self.length
            otherside = self.width
        else:
            bed_along_side = self.width
            otherside = self.length
        total_sections = 0
        bed_per_section = self.max_bed_per_section
        while bed_per_section > 0 and total_sections < min_sections:
            num_of_bed_along_otherside = int(
                ((otherside + self.path_width) / (self.bed_width + self.path_width))
            )
            sect_along_otherside = int(num_of_bed_along_otherside / bed_per_section)
            if sect_along_otherside == 0:
                bed_per_section = bed_per_section - 1
                continue
            else:
                num_of_bed_along_otherside = int(
                    num_of_bed_along_otherside
                    - (
                        (
                            (sect_along_otherside - 1)
                            * (self.path_width_btw_sections - self.path_width)
                        )
                        / (self.bed_width + self.path_width)
                    )
                )
                num_of_bed = int(num_of_bed_along_otherside) * num_of_bed_along_side
                total_sections = int(num_of_bed / bed_per_section)
                bed_per_section -= 1

        return (
            num_of_bed_along_otherside,
            bed_per_section + 1,
            total_sections,
        )

    def get_area_and_compost(
        self,
        bed_length: float,
        bed_along_side_name: str,
        num_of_bed_along_side: int,
        num_of_bed_along_otherside: int,
        bed_per_section: int,
        total_sections: int,
    ) -> tuple:
        """
        Calculates the area used in perecent and the compost requirements per
        bed and for the whole farm by the calculated parameters.

        params: Cropmap parameters calculated by the function `arrangement` and
                'num_of_sections`.

        returns: A tuple of area used (in %), compost
                 required per bed and total compost required for whole farm.
        """

        if bed_along_side_name == "length":
            bed_along_side = self.length
            otherside = self.width
        else:
            bed_along_side = self.width
            otherside = self.length
        total_area = round((bed_along_side * otherside), ROUND_TO)
        area_per_bed = self.bed_width * bed_length
        area_per_section = (bed_per_section * area_per_bed) + (
            bed_per_section - 1
        ) * bed_length * self.path_width
        total_area_of_path_btw_section = self.path_width_btw_sections * (
            ((num_of_bed_along_side - 1) * otherside)
            + (((total_sections / num_of_bed_along_side) - 1) * num_of_bed_along_side)
            * bed_length
        )
        total_area_used = round(
            (total_sections * area_per_section) + total_area_of_path_btw_section,
            ROUND_TO,
        )
        area_used_in_percent = round(((total_area_used * 100) / total_area), 2)

        # calculation for compost-required
        compost_required_per_bed = area_per_bed * self.compost_height_of_bed
        total_compost_required = (total_area_used * self.compost_height_of_path) + (
            (total_sections * bed_per_section)
            * (
                area_per_bed
                * (self.compost_height_of_bed - self.compost_height_of_path)
            )
        )
        compost_required_per_bed = round(compost_required_per_bed, ROUND_TO)
        total_compost_required = round(total_compost_required, ROUND_TO)

        return (
            area_used_in_percent,
            compost_required_per_bed,
            total_compost_required,
        )

    def best_arrangement(self, bed_along_length: list, bed_along_width: list) -> list:
        """
        Checks for the best arrangement by comparing Maximum Area used of
        arrangement along width and length.

        param:  bed_along_length and bed_along_width -> list of
                bed_length, bed_along_side_name, num_of_bed_along_side,
                bed_per_section, total_sections, area_used_in_percent,
                compost_required_per_bed, total_compost_required.

        returns: A list having best parameters.
        """

        if bed_along_length and bed_along_width:
            if bed_along_length[-3] > bed_along_width[-3]:  # comparing Area Used (%)
                return bed_along_length
            else:
                return bed_along_width
        return bed_along_width or bed_along_length

    def get_cropmap(self) -> list:
        """
        Calculates best parameters for cropmap that utilizes the maximum space
        on the basis of user defined constraints namely length, width, path_width,
        path_width_btw_sections, min_bed_length, max_bed_length, min_bed_per_section,
        max_bed_per_section, bed_width, compost_height_of_bed,
        compost_height_of_path.

        Based on the calculated it also calculates the compost required for
        newly formed market-garden and compost required for one bed.
        """

        # to handle the case where length or width are less than min bed length
        if self.length < self.min_bed_length or self.width < self.min_bed_length:
            min_sections = 1
        else:
            min_sections = 5

        # Step 1: To get arrangement with max bedlength (along the length and width)
        bed_along_length = self.arrangement(self.length, "length")
        bed_along_width = self.arrangement(self.width, "width")

        # Step 2: To get arrangement with maximum sections
        if bed_along_length:
            bed_along_length += self.num_of_section(*bed_along_length, min_sections)
            bed_along_length += self.get_area_and_compost(*bed_along_length)
        if bed_along_width:
            bed_along_width += self.num_of_section(*bed_along_width, min_sections)
            bed_along_width += self.get_area_and_compost(*bed_along_width)

        # Step 3: To get Best arrangement with maximum area used and also get
        # compost requirements
        calculated_params = self.best_arrangement(bed_along_length, bed_along_width)
        return calculated_params


if __name__ == "__main__":

    # Example Input: 50 60 0.4 0.7 5.0 25.0 1 10 0.75 0.3 0.1
    length, width = list(map(float, input("Enter farm dimensions (LxW): ").split(" ")))
    path_width = float(input("Enter path width: "))
    path_width_btw_sections = float(input("Enter path width between sections: "))
    min_bed_length = float(input("Enter min bed length: "))
    max_bed_length = float(input("Enter max bed length: "))
    min_bed_per_section = int(input("Enter min bed per section: "))
    max_bed_per_section = int(input("Enter max bed per secion: "))
    bed_width = float(input("Enter bed width: "))
    compost_height_of_bed = float(input("Enter compost height of bed: "))
    compost_height_of_path = float(input("Enter compost height of path: "))

    farm = Cropmap(
        length,
        width,
        path_width,
        path_width_btw_sections,
        min_bed_length,
        max_bed_length,
        min_bed_per_section,
        max_bed_per_section,
        bed_width,
        compost_height_of_bed,
        compost_height_of_path,
    )

    (
        bed_length,
        bed_along_side_name,
        num_of_bed_along_side,
        num_of_bed_along_otherside,
        bed_per_section,
        total_sections,
        area_used_in_percent,
        compost_required_per_bed,
        total_compost_required,
    ) = farm.get_cropmap()

    print(
        f"""
            No. of Sections = {total_sections}
            No. of Bed per Sections = {bed_per_section}
            Bed Length = {bed_length}
            Side Along which Bed are made = {bed_along_side_name}
            No. of bed along {bed_along_side_name} = {num_of_bed_along_side}
            No. of bed along other side = {num_of_bed_along_otherside}
            Total no. of beds = {num_of_bed_along_side*num_of_bed_along_otherside}
            Area Used(%) = {area_used_in_percent} %
            Compost Required for one bed = {compost_required_per_bed} cu.metre
            Compost Required for whole farm = {total_compost_required} cu.metre
        """
    )
