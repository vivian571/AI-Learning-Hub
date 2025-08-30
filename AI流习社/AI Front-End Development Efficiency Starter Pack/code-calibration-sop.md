# AI-Generated Code Calibration SOP Checklist

## 🔍 Pre-Deployment Quality Assurance Checklist

### ✅ 1. Security Audit
**Priority: CRITICAL**

#### Check for:
- [ ] **No Hardcoded Secrets**: Scan for API keys, passwords, tokens, or connection strings
  ```javascript
  // ❌ BAD: Hardcoded secret
  const API_KEY = "sk-1234567890abcdef";
  
  // ✅ GOOD: Environment variable
  const API_KEY = process.env.REACT_APP_API_KEY;
  ```

- [ ] **Input Validation**: Verify all user inputs are sanitized and validated
  ```javascript
  // Check for XSS prevention
  // ❌ BAD: Direct HTML insertion
  element.innerHTML = userInput;
  
  // ✅ GOOD: Proper sanitization
  element.textContent = userInput;
  // Or use DOMPurify for HTML content
  ```

- [ ] **SQL Injection Prevention**: Ensure parameterized queries or ORM usage
- [ ] **Authentication Checks**: Verify protected routes have proper auth guards
- [ ] **CORS Configuration**: Check for overly permissive CORS settings
- [ ] **Dependency Vulnerabilities**: Run `npm audit` or `yarn audit`

**Action Items**:
- Run security linter (ESLint security plugin)
- Use SAST tools (SonarQube, Snyk)
- Review authentication flow
- Check for exposed endpoints

---

### ✅ 2. Code Logic Verification
**Priority: HIGH**

#### Validate:
- [ ] **Business Logic Accuracy**: Ensure the code solves the intended problem
  - Test with edge cases
  - Verify mathematical calculations
  - Check conditional logic paths

- [ ] **State Management**: Verify state updates are predictable
  ```javascript
  // Check for race conditions
  // ❌ BAD: Direct state mutation
  state.items.push(newItem);
  
  // ✅ GOOD: Immutable update
  setState(prev => [...prev.items, newItem]);
  ```

- [ ] **Async Operations**: Check for proper async/await usage and error handling
- [ ] **Algorithm Efficiency**: Verify no unnecessary loops or operations
- [ ] **Data Flow**: Trace data from input to output for correctness

**Action Items**:
- Write unit tests for critical functions
- Test with boundary values
- Verify error scenarios
- Check for infinite loops

---

### ✅ 3. Performance Optimization
**Priority: HIGH**

#### Monitor:
- [ ] **Bundle Size**: Check if generated code adds excessive dependencies
  ```bash
  # Analyze bundle size
  npm run build
  npm run analyze
  ```

- [ ] **Render Performance**: Look for unnecessary re-renders
  ```javascript
  // ❌ BAD: Function recreated every render
  <Button onClick={() => handleClick(id)} />
  
  // ✅ GOOD: Memoized callback
  const handleClick = useCallback((id) => {...}, [dependencies]);
  ```

- [ ] **Memory Leaks**: Check for cleanup in useEffect/lifecycle methods
- [ ] **Network Requests**: Verify no redundant API calls
- [ ] **Lazy Loading**: Ensure code splitting where appropriate

**Action Items**:
- Run Lighthouse audit
- Profile with React DevTools/Vue DevTools
- Check network waterfall
- Measure Core Web Vitals

---

### ✅ 4. Error Handling & Resilience
**Priority: HIGH**

#### Implement:
- [ ] **Try-Catch Blocks**: Ensure async operations have error handling
  ```javascript
  // ✅ GOOD: Comprehensive error handling
  try {
    const data = await fetchData();
    setData(data);
  } catch (error) {
    console.error('Fetch failed:', error);
    setError(error.message);
    showNotification('Failed to load data');
  } finally {
    setLoading(false);
  }
  ```

- [ ] **Error Boundaries**: Implement error boundaries (React) or error handlers (Vue)
- [ ] **Fallback UI**: Provide graceful degradation for failures
- [ ] **Validation Errors**: Display user-friendly error messages
- [ ] **Network Failures**: Handle offline scenarios and timeouts

**Action Items**:
- Test with network throttling
- Simulate API failures
- Verify error messages are helpful
- Check logging implementation

---

### ✅ 5. Accessibility Compliance
**Priority: HIGH**

#### Ensure:
- [ ] **Semantic HTML**: Verify proper HTML element usage
  ```html
  <!-- ❌ BAD: Div as button -->
  <div onclick="submit()">Submit</div>
  
  <!-- ✅ GOOD: Semantic button -->
  <button type="submit">Submit</button>
  ```

- [ ] **ARIA Labels**: Check for appropriate ARIA attributes
- [ ] **Keyboard Navigation**: Test Tab order and keyboard interactions
- [ ] **Screen Reader Support**: Verify with screen reader tools
- [ ] **Color Contrast**: Ensure WCAG 2.1 AA compliance (4.5:1 ratio)
- [ ] **Focus Indicators**: Visible focus states for interactive elements

**Action Items**:
- Run axe DevTools audit
- Test with keyboard only
- Check with screen reader
- Validate color contrast ratios

---

### ✅ 6. Cross-Browser & Device Testing
**Priority: MEDIUM**

#### Test on:
- [ ] **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- [ ] **Mobile Devices**: iOS Safari, Chrome Android
- [ ] **Different Viewports**: Mobile (320px), Tablet (768px), Desktop (1920px)
- [ ] **Legacy Support**: Check IE11 if required
- [ ] **Progressive Enhancement**: Verify core functionality without JavaScript

**Action Items**:
- Use BrowserStack or similar service
- Test responsive breakpoints
- Check touch interactions
- Verify print styles if applicable

---

### ✅ 7. Code Style & Maintainability
**Priority: MEDIUM**

#### Review:
- [ ] **Naming Conventions**: Consistent and meaningful variable/function names
  ```javascript
  // ❌ BAD: Unclear naming
  const d = new Date();
  const yrs = calcYrs(d);
  
  // ✅ GOOD: Descriptive naming
  const currentDate = new Date();
  const yearsSinceStart = calculateYearsSince(currentDate);
  ```

- [ ] **Code Comments**: Adequate documentation for complex logic
- [ ] **DRY Principle**: No unnecessary code duplication
- [ ] **File Structure**: Logical component organization
- [ ] **Type Safety**: TypeScript types or PropTypes defined

**Action Items**:
- Run linter (ESLint/Prettier)
- Check for code smells
- Review with team standards
- Generate JSDoc documentation

---

### ✅ 8. Dependencies & Licensing
**Priority: MEDIUM**

#### Verify:
- [ ] **License Compatibility**: Check all dependencies for license conflicts
- [ ] **Dependency Size**: Evaluate if large libraries are necessary
- [ ] **Version Pinning**: Ensure package versions are locked
- [ ] **Security Updates**: Check for known vulnerabilities
- [ ] **Tree Shaking**: Verify unused code is eliminated

**Action Items**:
```bash
# Check licenses
npx license-checker

# Analyze dependencies
npx depcheck

# Check for updates
npm outdated
```

---

### ✅ 9. Testing Coverage
**Priority: HIGH**

#### Implement:
- [ ] **Unit Tests**: Core functions have tests
  ```javascript
  describe('calculateTotal', () => {
    it('should handle empty array', () => {
      expect(calculateTotal([])).toBe(0);
    });
    
    it('should sum correctly', () => {
      expect(calculateTotal([1, 2, 3])).toBe(6);
    });
    
    it('should handle negative numbers', () => {
      expect(calculateTotal([-1, 2])).toBe(1);
    });
  });
  ```

- [ ] **Integration Tests**: Component interactions tested
- [ ] **E2E Tests**: Critical user paths covered
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Coverage Metrics**: Aim for >80% code coverage

**Action Items**:
- Write test cases
- Run coverage report
- Test error scenarios
- Implement snapshot tests

---

### ✅ 10. Documentation & Deployment Readiness
**Priority: MEDIUM**

#### Complete:
- [ ] **README Updates**: Document setup and usage instructions
- [ ] **API Documentation**: Document endpoints and data contracts
- [ ] **Environment Variables**: Document all required env vars
  ```markdown
  ## Environment Variables
  - `REACT_APP_API_URL`: Backend API endpoint
  - `REACT_APP_AUTH_DOMAIN`: Auth0 domain
  - `REACT_APP_CLIENT_ID`: OAuth client ID
  ```

- [ ] **Deployment Guide**: Include build and deployment steps
- [ ] **Change Log**: Document what the AI-generated code adds/modifies
- [ ] **Known Issues**: List any limitations or pending fixes

**Action Items**:
- Update README.md
- Create .env.example
- Document breaking changes
- Add inline code comments

---

## 📋 Quick Reference Checklist

Use this for rapid review:

```markdown
□ No hardcoded secrets or API keys
□ Input validation and sanitization implemented
□ Async operations have error handling
□ No unnecessary re-renders or memory leaks
□ Accessibility audit passed (WCAG 2.1 AA)
□ Tested on multiple browsers and devices
□ Code follows team style guide
□ Dependencies are secure and necessary
□ Unit tests written and passing
□ Documentation is complete and accurate
```

## 🚨 Red Flags to Immediately Address

1. **eval() or Function() constructor usage**
2. **innerHTML with user input**
3. **Disabled ESLint rules without justification**
4. **HTTP requests in production code**
5. **Console.log statements left in code**
6. **TODO comments indicating incomplete features**
7. **Deprecated method usage**
8. **Missing error boundaries**
9. **Infinite loops or recursion without base case**
10. **Direct DOM manipulation in React/Vue components**

## 🎯 Final Verification

Before deploying AI-generated code:

1. **Peer Review**: Have another developer review the code
2. **Staging Test**: Deploy to staging environment first
3. **Monitor Metrics**: Set up monitoring for errors and performance
4. **Rollback Plan**: Ensure you can quickly revert if issues arise
5. **User Acceptance**: Get stakeholder approval on functionality

---

*Remember: AI-generated code is a starting point. Always apply human expertise to ensure production readiness.*