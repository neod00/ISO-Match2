// InsightMatch2 Frontend JavaScript

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',
    BACKEND_URL: 'http://localhost:8000'
};

// Utility Functions
function byId(id) {
    return document.getElementById(id);
}

function showElement(element) {
    if (element) element.style.display = 'block';
}

function hideElement(element) {
    if (element) element.style.display = 'none';
}

function setLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// API Functions
async function callAPI(endpoint, options = {}) {
    try {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Analysis Functions
function initAnalysis() {
    const form = byId('analysis-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const homepage = byId('homepage').value.trim();
        const email = byId('email').value.trim();
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (!homepage || !email) {
            alert('홈페이지 URL과 이메일을 모두 입력해주세요.');
            return;
        }

        try {
            setLoading(submitBtn, true);
            
            // Store data for consultant matching
            localStorage.setItem('im:last_homepage', homepage);
            localStorage.setItem('im:last_email', email);
            
            // Call analysis API
            const result = await callAPI('/analyze', {
                method: 'POST',
                body: JSON.stringify({ homepage, email })
            });
            
            if (result.success) {
                displayAnalysisResult(result.data);
            } else {
                throw new Error(result.error || '분석 중 오류가 발생했습니다.');
            }
            
        } catch (error) {
            console.error('Analysis failed:', error);
            alert('분석 중 오류가 발생했습니다. 다시 시도해주세요.');
        } finally {
            setLoading(submitBtn, false);
        }
    });
}

function displayAnalysisResult(data) {
    const resultSection = byId('analysis-result');
    if (!resultSection) return;

    // Update basic info
    byId('analysis-company').textContent = data.company || 'Unknown';
    byId('analysis-date').textContent = data.analysis_date || 'Unknown';
    byId('analysis-method').textContent = data.analysis_method || 'Unknown';
    
    // Update summary
    byId('summary').textContent = data.summary || '요약을 불러올 수 없습니다.';
    
    // Update risks
    const risksList = byId('risks');
    if (risksList) {
        risksList.innerHTML = '';
        (data.risks || []).forEach(risk => {
            const li = document.createElement('li');
            li.textContent = risk;
            risksList.appendChild(li);
        });
    }
    
    // Update certifications
    const certsList = byId('certifications');
    if (certsList) {
        certsList.innerHTML = '';
        (data.certifications || []).forEach(cert => {
            const li = document.createElement('li');
            li.textContent = cert;
            certsList.appendChild(li);
        });
    }
    
    // Update news
    const newsList = byId('news-list');
    if (newsList) {
        newsList.innerHTML = '';
        (data.news || []).forEach(news => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${news.url}" target="_blank" rel="noopener">${news.title}</a>
                <div class="muted">${news.snippet}</div>
            `;
            newsList.appendChild(li);
        });
    }
    
    // Update DART
    const dartList = byId('dart-list');
    if (dartList) {
        dartList.innerHTML = '';
        (data.dart || []).forEach(dart => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${dart.url}" target="_blank" rel="noopener">${dart.title}</a>
                <div class="muted">${dart.snippet}</div>
            `;
            dartList.appendChild(li);
        });
    }
    
    // Update DART more link
    const dartMore = byId('dart-more');
    if (dartMore && data.company) {
        dartMore.href = `https://dart.fss.or.kr/dsab007/main.do?selectDate=&textCrpNm=${encodeURIComponent(data.company)}`;
    }
    
    // Show result section
    showElement(resultSection);
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Consultant Functions
function initConsultants() {
    const consultantList = byId('consultant-list');
    if (!consultantList) return;

    // Load consultants on page load
    loadConsultants();
    
    // Setup filters
    const filters = ['filter-industry', 'filter-cert', 'filter-region'];
    filters.forEach(filterId => {
        const filter = byId(filterId);
        if (filter) {
            filter.addEventListener('change', loadConsultants);
        }
    });
}

async function loadConsultants() {
    try {
        const industry = byId('filter-industry')?.value || '';
        const certification = byId('filter-cert')?.value || '';
        const region = byId('filter-region')?.value || '';
        
        const params = new URLSearchParams();
        if (industry) params.append('industry', industry);
        if (certification) params.append('certification', certification);
        if (region) params.append('region', region);
        
        const result = await callAPI(`/consultants?${params.toString()}`);
        
        if (result.success) {
            displayConsultants(result.data);
            updateResultsCount(result.data.length);
        } else {
            throw new Error(result.error || '컨설턴트 조회 중 오류가 발생했습니다.');
        }
        
    } catch (error) {
        console.error('Failed to load consultants:', error);
        displayConsultants([]);
        updateResultsCount(0);
    }
}

function displayConsultants(consultants) {
    const consultantList = byId('consultant-list');
    const noResults = byId('no-results');
    
    if (!consultantList) return;
    
    consultantList.innerHTML = '';
    
    if (consultants.length === 0) {
        showElement(noResults);
        return;
    }
    
    hideElement(noResults);
    
    consultants.forEach(consultant => {
        const card = createConsultantCard(consultant);
        consultantList.appendChild(card);
    });
}

function createConsultantCard(consultant) {
    const card = document.createElement('article');
    card.className = 'consultant-card';
    
    const ratingStars = '★'.repeat(Math.floor(consultant.rating)) + '☆'.repeat(5 - Math.floor(consultant.rating));
    
    card.innerHTML = `
        <div class="consultant-header">
            <div class="consultant-name">${consultant.name}</div>
            <div class="consultant-rating">${ratingStars} ${consultant.rating}</div>
        </div>
        <div class="consultant-info">
            경력 ${consultant.years}년 · ${consultant.industry} · ${consultant.region}
        </div>
        <div class="consultant-certs">
            ${(consultant.certifications || []).map(cert => 
                `<span class="cert-tag">${cert}</span>`
            ).join('')}
        </div>
        <div class="consultant-actions">
            <button class="btn btn-primary" onclick="requestConsultation(${consultant.id})">상담 요청</button>
        </div>
    `;
    
    return card;
}

function updateResultsCount(count) {
    const countElement = byId('results-count');
    if (countElement) {
        countElement.textContent = `${count}명의 컨설턴트`;
    }
}

function clearFilters() {
    const filters = ['filter-industry', 'filter-cert', 'filter-region'];
    filters.forEach(filterId => {
        const filter = byId(filterId);
        if (filter) filter.value = '';
    });
    loadConsultants();
}

function requestConsultation(consultantId) {
    alert(`컨설턴트 ID ${consultantId}에 대한 상담 요청 기능은 준비 중입니다.`);
}

// Registration Functions
function initRegistration() {
    const form = byId('register-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Get selected certifications
        const certifications = Array.from(form.querySelectorAll('input[name="certifications"]:checked'))
            .map(input => input.value);
        
        data.certifications = certifications;
        
        if (data.certifications.length === 0) {
            alert('최소 하나의 인증을 선택해주세요.');
            return;
        }
        
        try {
            const result = await callAPI('/consultants', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (result.success) {
                showRegistrationSuccess();
                form.reset();
            } else {
                throw new Error(result.error || '등록 중 오류가 발생했습니다.');
            }
            
        } catch (error) {
            console.error('Registration failed:', error);
            alert('등록 중 오류가 발생했습니다. 다시 시도해주세요.');
        }
    });
}

function showRegistrationSuccess() {
    const successMsg = byId('register-success');
    const form = byId('register-form');
    
    if (successMsg) {
        showElement(successMsg);
        successMsg.scrollIntoView({ behavior: 'smooth' });
    }
    
    if (form) {
        hideElement(form);
    }
}

function resetForm() {
    const form = byId('register-form');
    if (form) {
        form.reset();
    }
}

// DART Filter Functions
function initDartFilter() {
    const dartFilter = byId('dart-filter');
    if (!dartFilter) return;
    
    dartFilter.addEventListener('change', filterDartItems);
}

function filterDartItems() {
    const filter = byId('dart-filter');
    const dartList = byId('dart-list');
    
    if (!filter || !dartList) return;
    
    const filterValue = filter.value;
    const items = dartList.querySelectorAll('li');
    
    items.forEach(item => {
        const title = item.querySelector('a')?.textContent || '';
        const shouldShow = !filterValue || title.includes(filterValue);
        item.style.display = shouldShow ? 'block' : 'none';
    });
}

// Initialize page based on current page
function initPage() {
    const currentPage = window.location.pathname.split('/').pop();
    
    switch (currentPage) {
        case 'analysis.html':
            initAnalysis();
            initDartFilter();
            break;
        case 'consultants.html':
            initConsultants();
            break;
        case 'consultant-register.html':
            initRegistration();
            break;
        default:
            // Index page or other pages
            break;
    }
}

// Global functions for HTML onclick handlers
window.clearFilters = clearFilters;
window.requestConsultation = requestConsultation;
window.resetForm = resetForm;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initPage);
