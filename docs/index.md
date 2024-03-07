---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Supernest"
  text: "Nested sampling accelerated"
  tagline: Supernest accelerates typical nested sampling workflows by including a proposal prior and reducing the Kullback-Leibler divergence.
  actions:
    - theme: alt
      text: API Documentation
      link: /api-docs

features:
  - title: Drop-in
    details: Adding `supernest` is as easy as wrapping your priors.
  - title: Risk-free
    details: If your proposal is somehow inadequate, `supernest` falls back onto the original prior and you get your results.
  - title: Fast
    details: When the proposal is correct-enough, you can expect the acceleration to be by a factor of hundreds.
---
