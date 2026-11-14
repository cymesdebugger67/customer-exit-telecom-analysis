# Assumptions and Limitations

## Assumptions

The analysis assumes that:

- Each customer ID represents one unique customer.
- `Churn = Yes` identifies a customer who left the service.
- Recorded contract and service categories are internally valid.
- Zero-tenure customers with blank TotalCharges should be retained.
- Blank TotalCharges values should be represented as missing rather
  than assumed to equal zero.
- Segment-level churn rates are appropriate descriptive indicators.

## Limitations

The IBM Telco dataset is a historical sample.

The project does not claim that its results represent the current
telecommunications market.

Observed relationships are associations rather than causal effects.

For example, elevated churn among fiber optic customers does not
prove that fiber optic service causes churn.

Unobserved variables may influence the results, including:

- Customer satisfaction
- Service outages
- Competitor pricing
- Geographic location
- Customer-service interactions
- Promotional offers
- Acquisition channel

## Segment Interpretation

Small groups can produce unstable percentages.

The highest-risk combined-segment ranking therefore applies a
minimum customer-count threshold.

Business priority should consider both:

- churn rate
- customer volume

## Recommendations

Recommendations in this project identify areas for further business
investigation.

They are not validated interventions.

A real organization should test retention actions through controlled
experiments or other appropriate evaluation methods.
