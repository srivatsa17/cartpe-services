import { screen, render, fireEvent, waitFor, cleanup } from '@testing-library/react';
import Rating from '../src/components/Rating';


describe("Rating component", () => {

    const text = '12 reviews';

    afterEach(() => {
        cleanup();
    })

    test("Check for stars", () => {
        render(
            <Rating rating={4.5} text={text}/>
        );
        expect(screen.getByTestId("ratings")).toBeInTheDocument();
    });

    test("Check for tooltip", () => {
        render(
            <Rating rating={4.5} text={text}/>
        );
        fireEvent.mouseOver(screen.getByTestId("ratings"));
        waitFor(() => expect(screen.findByText("4.5 out of 5 stars")).toBeInTheDocument());
    });

    test("Check for only empty stars", () => {
        render(
            <Rating rating={0} text={text}/>
        );
        expect(screen.queryByTestId("full-star")).not.toBeInTheDocument();
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        waitFor(() => expect(screen.getAllByTestId("empty-star")).toBeInTheDocument());
    })

    test("Check for one full star and others to be empty stars", () => {
        render(
            <Rating rating={1} text={text}/>
        );
        expect(screen.getByTestId("full-star")).toBeInTheDocument();
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        waitFor(() => expect(screen.queryAllByTestId("empty-star")).toBeInTheDocument());
    })

    test("Check for full, half and empty star", () => {
        render(
            <Rating rating={2.6} text={text}/>
        );
        waitFor(() => expect(screen.getAllByTestId("full-star")).toBeInTheDocument());
        expect(screen.queryByTestId("half-star")).toBeInTheDocument();
        waitFor(() => expect(screen.queryAllByTestId("empty-star")).toBeInTheDocument());
    })

    test("Check for full stars and one empty star", () => {
        render(
            <Rating rating={4.3} text={text}/>
        );
        waitFor(() => expect(screen.getAllByTestId("full-star")).toBeInTheDocument());
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        expect(screen.queryByTestId("empty-star")).toBeInTheDocument();
    })

    test("Check for all full stars", () => {
        render(
            <Rating rating={5} text={text}/>
        );
        waitFor(() => expect(screen.getAllByTestId("full-star")).toBeInTheDocument());
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        expect(screen.queryByTestId("empty-star")).not.toBeInTheDocument();
    })

    test("Check for rating greater than 5", () => {
        render(
            <Rating rating={7.7} text={text}/>
        );
        waitFor(() => expect(screen.getAllByTestId("full-star")).toBeInTheDocument());
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        expect(screen.queryByTestId("empty-star")).not.toBeInTheDocument();
    })

    test("Check for rating lesser than 0", () => {
        render(
            <Rating rating={-1} text={text}/>
        );
        expect(screen.queryByTestId("full-star")).not.toBeInTheDocument();
        expect(screen.queryByTestId("half-star")).not.toBeInTheDocument();
        waitFor(() => expect(screen.getAllTestId("empty-star")).toBeInTheDocument());
    })

    test("Check for valid review count", () => {
        render(
            <Rating rating={3} text={text}/>
        );
        expect(screen.queryByTestId("review-count")).toBeInTheDocument();
    })

    test("Check for null rating count", () => {
        render(
            <Rating rating={3}/>
        );
        expect(screen.queryByTestId("review-count")).toBeNull();
    })

    test("Check for empty rating count", () => {
        render(
            <Rating rating={3} text={""}/>
        );
        expect(screen.queryByTestId("review-count")).toBeNull();
    })
});