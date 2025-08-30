# Golden Prompt Templates for AI Front-End Development

## 🎯 React Component Development

### Basic Component Creation
```
Create a React component called [ComponentName] that:
- Uses functional components with TypeScript
- Implements [specific functionality]
- Uses React hooks (useState, useEffect as needed)
- Follows accessibility best practices with proper ARIA labels
- Includes proper error handling and loading states
- Uses Tailwind CSS for styling with responsive design
- Exports with proper TypeScript interfaces for props
- Includes JSDoc comments for component documentation
```

### Complex State Management
```
Build a React component with advanced state management that:
- Implements [feature description]
- Uses useReducer for complex state logic
- Includes optimistic UI updates
- Handles async operations with proper error boundaries
- Implements debouncing/throttling where appropriate
- Uses React.memo for performance optimization
- Includes unit test setup with Jest/React Testing Library
- Follows the principle of single responsibility
```

## 🎯 Vue.js Development

### Vue 3 Composition API Component
```
Create a Vue 3 component using Composition API that:
- Named [ComponentName] with TypeScript support
- Implements [specific functionality]
- Uses script setup syntax
- Includes reactive state with ref/reactive
- Implements computed properties and watchers as needed
- Uses Tailwind CSS with scoped styles
- Includes proper props validation with TypeScript
- Handles lifecycle hooks appropriately
- Exports types for external usage
```

### Vuex/Pinia Store Module
```
Design a [Vuex/Pinia] store module for [feature name] that:
- Manages [data type] state
- Includes TypeScript typing throughout
- Implements getters for derived state
- Creates actions for async operations with error handling
- Uses mutations (Vuex) or direct state updates (Pinia)
- Includes API integration with axios/fetch
- Implements optimistic updates where appropriate
- Follows Vue 3 best practices for reactivity
```

## 🎯 Full-Stack Integration

### Next.js Page with API Route
```
Create a Next.js page with TypeScript that:
- Implements [page functionality]
- Uses App Router (Next.js 14+) conventions
- Includes server components where appropriate
- Implements client components with 'use client' directive
- Creates corresponding API route in app/api folder
- Uses Prisma/Drizzle for database operations
- Implements proper error handling and loading states
- Includes SEO metadata and OpenGraph tags
- Uses Tailwind CSS with CSS modules if needed
- Implements proper data fetching with cache strategies
```

### API Integration Layer
```
Build a TypeScript API service layer that:
- Connects to [API endpoint/service]
- Uses axios/fetch with proper typing
- Implements request/response interceptors
- Includes automatic retry logic with exponential backoff
- Handles authentication tokens and refresh logic
- Implements proper error handling with custom error classes
- Includes request cancellation support
- Uses environment variables for configuration
- Implements response caching where appropriate
- Follows RESTful or GraphQL best practices
```

## 🎯 UI/UX Implementation

### Responsive Design System Component
```
Create a responsive [component type] that:
- Follows [design system name] guidelines
- Implements mobile-first responsive design
- Uses CSS Grid/Flexbox appropriately
- Includes dark mode support with CSS variables
- Implements smooth animations with Framer Motion/CSS
- Ensures WCAG 2.1 AA accessibility compliance
- Supports keyboard navigation
- Includes focus management for modals/drawers
- Uses semantic HTML elements
- Implements loading skeletons for better UX
```

### Form with Validation
```
Build a form component that:
- Implements [form purpose]
- Uses react-hook-form/Formik (React) or VeeValidate (Vue)
- Includes client-side validation with Zod/Yup
- Implements server-side validation handling
- Shows inline error messages with proper styling
- Includes progress indicators for multi-step forms
- Implements auto-save functionality
- Handles file uploads if needed
- Prevents double submission
- Includes success/error toast notifications
```

## 🎯 Performance & Optimization

### Performance-Optimized List
```
Create a virtualized list component that:
- Renders [data type] items efficiently
- Implements virtual scrolling for large datasets
- Uses react-window/react-virtualized (React) or vue-virtual-scroll
- Includes search/filter functionality with debouncing
- Implements lazy loading for images
- Uses intersection observer for infinite scroll
- Includes sorting capabilities
- Implements selection (single/multi) if needed
- Caches rendered items appropriately
- Handles empty states and error states
```

### Code Splitting Implementation
```
Implement code splitting for [application section] that:
- Uses dynamic imports with React.lazy/Vue defineAsyncComponent
- Implements route-based code splitting
- Includes proper loading states with Suspense
- Implements error boundaries for failed chunks
- Uses webpack magic comments for chunk naming
- Preloads critical chunks
- Implements progressive enhancement
- Monitors bundle size impact
- Uses tree shaking effectively
```

## 🎯 Testing & Documentation

### Component Testing Suite
```
Write comprehensive tests for [component name] that:
- Uses Jest and React Testing Library/Vue Test Utils
- Includes unit tests for all props variations
- Tests user interactions and events
- Includes integration tests with mocked API calls
- Tests error states and edge cases
- Includes accessibility testing with jest-axe
- Tests responsive behavior
- Includes snapshot tests for UI consistency
- Achieves >80% code coverage
- Uses MSW for API mocking
```

### Storybook Documentation
```
Create Storybook stories for [component] that:
- Includes all component variants
- Documents all props with descriptions
- Includes interactive controls (knobs/controls)
- Shows different states (loading, error, success)
- Includes usage examples with code snippets
- Documents accessibility features
- Includes responsive preview options
- Shows theme variations if applicable
- Includes performance metrics
- Documents keyboard shortcuts
```

## 💡 Pro Tips for Using These Templates

1. **Be Specific**: Replace placeholders with exact requirements
2. **Add Context**: Include business logic or design requirements
3. **Specify Versions**: Mention specific library versions if needed
4. **Include Examples**: Provide sample data structures or API responses
5. **Define Constraints**: Mention performance budgets or browser support
6. **Request Documentation**: Always ask for inline comments and README updates
7. **Iterate**: Start with basic implementation, then refine with follow-up prompts
8. **Review Output**: Always review AI-generated code for security and best practices