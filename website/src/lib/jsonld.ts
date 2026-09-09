import { doctor } from '@/data/doctor';
import { clinics, sessionTimes, weekdays } from '@/data/clinics';

const dayMap: Record<string, string> = {
  週一: 'Monday',
  週二: 'Tuesday',
  週三: 'Wednesday',
  週四: 'Thursday',
  週五: 'Friday',
  週六: 'Saturday',
  週日: 'Sunday',
};

export function physicianJsonLd(site: URL | undefined, imageUrl?: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Physician',
    '@id': new URL('/about/#physician', site).toString(),
    name: doctor.displayName,
    alternateName: doctor.englishName,
    url: new URL('/about/', site).toString(),
    image: imageUrl,
    jobTitle: doctor.jobTitle,
    medicalSpecialty: ['SportsMedicine', 'PrimaryCare'],
    worksFor: { '@type': 'Hospital', name: doctor.hospital },
    affiliation: clinics.map((c) => ({ '@type': 'MedicalClinic', name: c.name, address: c.address })),
    alumniOf: { '@type': 'CollegeOrUniversity', name: '國防醫學院' },
    knowsLanguage: doctor.languages,
    sameAs: [doctor.social.facebook.url, doctor.social.threads.url, doctor.social.instagram.url, doctor.social.blog.url],
  };
}

export function clinicsJsonLd(site: URL | undefined) {
  return clinics.map((c) => {
    const hours = weekdays.flatMap((d) =>
      (c.schedule[d] ?? []).map((s) => {
        const [opens, closes] = sessionTimes[s].time.split('–');
        return { '@type': 'OpeningHoursSpecification', dayOfWeek: dayMap[d], opens, closes };
      }),
    );
    return {
      '@context': 'https://schema.org',
      '@type': 'MedicalClinic',
      name: `${c.name} ${c.department}（程皓醫師門診）`,
      address: { '@type': 'PostalAddress', streetAddress: c.address, addressCountry: 'TW' },
      telephone: c.phone,
      url: new URL('/clinic/', site).toString(),
      openingHoursSpecification: hours,
      employee: { '@id': new URL('/about/#physician', site).toString() },
    };
  });
}

export function breadcrumbJsonLd(site: URL | undefined, items: { label: string; href?: string }[]) {
  const all = [{ label: '首頁', href: '/' }, ...items];
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: all.map((c, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: c.label,
      item: c.href ? new URL(c.href, site).toString() : undefined,
    })),
  };
}
