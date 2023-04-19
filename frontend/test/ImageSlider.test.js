import { screen, render, fireEvent, waitFor, cleanup } from '@testing-library/react';
import ImageSlider from "../src/components/ImageSlider";

describe("Image Slider Component", () => {
    beforeEach(() => {

        const product = {
            '_id': '1',
            'name': 'Airpods Wireless Bluetooth Headphones',
            'image': '/images/airpods.jpg',
        }

        return render(
            <ImageSlider product={product}/>
        );
    });

    afterEach(() => {
        cleanup();
    })

    test("Check for presence of left slider arrow", () => {
        expect(screen.getByTestId("slide-left-arrow")).toBeInTheDocument();
    });

    test("Check for presence of right slider arrow", () => {
        expect(screen.getByTestId("slide-right-arrow")).toBeInTheDocument();
    });

    test("Check for product images existence", () => {
        waitFor(() => expect(screen.getAllByTestId("images")).toBeInTheDocument());
    })

    test("Check for left scrolling", () => {
        expect(screen.getByTestId("slider").scrollLeft).toBe(0);
        fireEvent.click(screen.getByTestId("slide-right-arrow"));
        fireEvent.click(screen.getByTestId("slide-right-arrow"));
        fireEvent.click(screen.getByTestId("slide-left-arrow"));
        expect(screen.getByTestId("slider").scrollLeft).toBe(145);
    });

    test("Check for right scrolling", () => {
        expect(screen.getByTestId("slider").scrollLeft).toBe(0);
        fireEvent.click(screen.getByTestId("slide-right-arrow"));
        expect(screen.getByTestId("slider").scrollLeft).toBe(145);
    });

    test("Check for featured image", async () => {
        const initialImageSource = "http://localhost/images/airpods.jpg";
        const changedImageSource = "http://localhost/images/alexa.jpg";

        expect(screen.getByTestId("featured-image").src).toBe(initialImageSource);
        fireEvent.mouseOver(screen.getAllByTestId("product-images")[0]);
        expect(await screen.getByTestId("featured-image").src).toBe(changedImageSource);
    });
});