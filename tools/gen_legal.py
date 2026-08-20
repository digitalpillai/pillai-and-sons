"""
gen_legal.py  —  V1
The Privacy Policy and the Terms and Conditions, transcribed from the two Word
documents the client supplied on 20 August 2026.

This is the client's own legal text. Three classes of edit were made to it, all
agreed beforehand:

  * "Toyota/Hero" -> "Maruti Suzuki", six places. The document had been adapted
    from another dealer's template and the find-replace had missed them; left
    alone the page would have named the wrong manufacturer.
  * "Pillai & Sos" -> "Pillai & Sons", two places — a typo of the company's own
    name.
  * '".ord" suffix' -> '".org" suffix' — enthusiast domains take .org.

One formatting repair: in the Terms, the definitions of "Website" and "You" had
run together into a single paragraph in the source file. They are separated here.

Nothing else was reworded, reordered or removed. The Word documents are the
source of record; if they change, change this file to match rather than editing
the generated HTML.

Block kinds:  h2 / h3 headings, p paragraphs, meta for the "last updated" line,
dl for the defined-terms list in the Terms.
"""

TERMS = [
    ("meta", "Last updated: August 19, 2026"),
    ("p", "Please read these terms and conditions carefully before using Our Service."),
    ("h2", "Interpretation and Definitions"),
    ("h3", "Interpretation"),
    ("p", "The words of which the initial letter is capitalized have meanings defined under the "
     "following conditions. The following definitions shall have the same meaning "
     "regardless of whether they appear in singular or in plural."),
    ("h3", "Definitions"),
    ("p", "For the purposes of these Terms and Conditions:"),
    ("dl", [
        ("Affiliate",
         "means an entity that controls, is controlled by or is under common control with a "
         "party, where \"control\" means ownership of 50% or more of the shares, equity interest "
         "or other securities entitled to vote for election of directors or other managing "
         "authority."),
        ("Country",
         "refers to: Tamil Nadu, India"),
        ("Company",
         "(referred to as either \"the Company\", \"We\", \"Us\" or \"Our\" in this Agreement) refers "
         "to Pillai & Sons Motor Company, 31-A, Medical College Road, Rajjappa Nagar, "
         "Jayalakshmi Nagar, Thanjavur, Tamil Nadu, 613007"),
        ("Device",
         "means any device that can access the Service such as a computer, a cellphone or a "
         "digital tablet."),
        ("Service",
         "refers to the Website."),
        ("Terms and Conditions",
         "(also referred as \"Terms\") mean these Terms and Conditions that form the entire "
         "agreement between You and the Company regarding the use of the Service."),
        ("Third-party Social Media Service",
         "means any services or content (including data, information, products or services) "
         "provided by a third-party that may be displayed, included or made available by the "
         "Service."),
        ("Website",
         "refers to Pillai & Sons Motor Company, accessible from https://pillaiandsons.in"),
        ("You",
         "means the individual accessing or using the Service, or the company, or other legal "
         "entity on behalf of which such individual is accessing or using the Service, as "
         "applicable."),
    ]),
    ("h2", "Acknowledgment"),
    ("p", "These are the Terms and Conditions governing the use of this Service and the "
     "agreement that operates between You and the Company. These Terms and Conditions set "
     "out the rights and obligations of all users regarding the use of the Service."),
    ("p", "Your access to and use of the Service is conditioned on Your acceptance of and "
     "compliance with these Terms and Conditions. These Terms and Conditions apply to all "
     "visitors, users and others who access or use the Service."),
    ("p", "By accessing or using the Service You agree to be bound by these Terms and "
     "Conditions. If You disagree with any part of these Terms and Conditions then You may "
     "not access the Service."),
    ("p", "You represent that you are over the age of 18. The Company does not permit those "
     "under 18 to use the Service."),
    ("p", "Your access to and use of the Service is also conditioned on Your acceptance of and "
     "compliance with the Privacy Policy of the Company. Our Privacy Policy describes Our "
     "policies and procedures on the collection, use and disclosure of Your personal "
     "information when You use the Application or the Website and tells You about Your "
     "privacy rights and how the law protects You. Please read Our Privacy Policy "
     "carefully before using Our Service."),
    ("h2", "Links to Other Websites"),
    ("p", "Our Service may contain links to third-party web sites or services that are not "
     "owned or controlled by the Company."),
    ("p", "The Company has no control over, and assumes no responsibility for, the content, "
     "privacy policies, or practices of any third party web sites or services. You further "
     "acknowledge and agree that the Company shall not be responsible or liable, directly "
     "or indirectly, for any damage or loss caused or alleged to be caused by or in "
     "connection with the use of or reliance on any such content, goods or services "
     "available on or through any such web sites or services."),
    ("p", "We strongly advise You to read the terms and conditions and privacy policies of any "
     "third-party web sites or services that You visit."),
    ("h2", "Termination"),
    ("p", "We may terminate or suspend Your access immediately, without prior notice or "
     "liability, for any reason whatsoever, including without limitation if You breach "
     "these Terms and Conditions."),
    ("p", "Upon termination, Your right to use the Service will cease immediately."),
    ("h2", "Limitation of Liability"),
    ("p", "Notwithstanding any damages that You might incur, the entire liability of the "
     "Company and any of its suppliers under any provision of this Terms and Your "
     "exclusive remedy for all of the foregoing shall be limited to the amount actually "
     "paid by You through the Service or 100 USD if You haven't purchased anything through "
     "the Service."),
    ("p", "To the maximum extent permitted by applicable law, in no event shall the Company or "
     "its suppliers be liable for any special, incidental, indirect, or consequential "
     "damages whatsoever (including, but not limited to, damages for loss of profits, loss "
     "of data or other information, for business interruption, for personal injury, loss "
     "of privacy arising out of or in any way related to the use of or inability to use "
     "the Service, third-party software and/or third-party hardware used with the Service, "
     "or otherwise in connection with any provision of this Terms), even if the Company or "
     "any supplier has been advised of the possibility of such damages and even if the "
     "remedy fails of its essential purpose."),
    ("p", "Some states do not allow the exclusion of implied warranties or limitation of "
     "liability for incidental or consequential damages, which means that some of the "
     "above limitations may not apply. In these states, each party's liability will be "
     "limited to the greatest extent permitted by law."),
    ("h2", "\"AS IS\" and \"AS AVAILABLE\" Disclaimer"),
    ("p", "The Service is provided to You \"AS IS\" and \"AS AVAILABLE\" and with all faults and "
     "defects without warranty of any kind. To the maximum extent permitted under "
     "applicable law, the Company, on its own behalf and on behalf of its Affiliates and "
     "its and their respective licensors and service providers, expressly disclaims all "
     "warranties, whether express, implied, statutory or otherwise, with respect to the "
     "Service, including all implied warranties of merchantability, fitness for a "
     "particular purpose, title and non-infringement, and warranties that may arise out of "
     "course of dealing, course of performance, usage or trade practice. Without "
     "limitation to the foregoing, the Company provides no warranty or undertaking, and "
     "makes no representation of any kind that the Service will meet Your requirements, "
     "achieve any intended results, be compatible or work with any other software, "
     "applications, systems or services, operate without interruption, meet any "
     "performance or reliability standards or be error free or that any errors or defects "
     "can or will be corrected."),
    ("p", "Without limiting the foregoing, neither the Company nor any of the company's "
     "provider makes any representation or warranty of any kind, express or implied: (i) "
     "as to the operation or availability of the Service, or the information, content, and "
     "materials or products included thereon; (ii) that the Service will be uninterrupted "
     "or error-free; (iii) as to the accuracy, reliability, or currency of any information "
     "or content provided through the Service; or (iv) that the Service, its servers, the "
     "content, or e-mails sent from or on behalf of the Company are free of viruses, "
     "scripts, trojan horses, worms, malware, timebombs or other harmful components."),
    ("p", "Some jurisdictions do not allow the exclusion of certain types of warranties or "
     "limitations on applicable statutory rights of a consumer, so some or all of the "
     "above exclusions and limitations may not apply to You. But in such a case the "
     "exclusions and limitations set forth in this section shall be applied to the "
     "greatest extent enforceable under applicable law."),
    ("h2", "Governing Law"),
    ("p", "The laws of the Country, excluding its conflicts of law rules, shall govern this "
     "Terms and Your use of the Service. Your use of the Application may also be subject "
     "to other local, state, national, or international laws."),
    ("h2", "Disputes Resolution"),
    ("p", "If You have any concern or dispute about the Service, You agree to first try to "
     "resolve the dispute informally by contacting the Company."),
    ("h2", "For European Union (EU) Users"),
    ("p", "If You are a European Union consumer, you will benefit from any mandatory provisions "
     "of the law of the country in which You are resident."),
    ("h2", "United States Legal Compliance"),
    ("p", "You represent and warrant that (i) You are not located in a country that is subject "
     "to the United States government embargo, or that has been designated by the United "
     "States government as a \"terrorist supporting\" country, and (ii) You are not listed "
     "on any United States government list of prohibited or restricted parties."),
    ("h2", "Severability and Waiver"),
    ("h3", "Severability"),
    ("p", "If any provision of these Terms is held to be unenforceable or invalid, such "
     "provision will be changed and interpreted to accomplish the objectives of such "
     "provision to the greatest extent possible under applicable law and the remaining "
     "provisions will continue in full force and effect."),
    ("h3", "Waiver"),
    ("p", "Except as provided herein, the failure to exercise a right or to require performance "
     "of an obligation under these Terms shall not affect a party's ability to exercise "
     "such right or require such performance at any time thereafter nor shall the waiver "
     "of a breach constitute a waiver of any subsequent breach."),
    ("h2", "Translation Interpretation"),
    ("p", "These Terms and Conditions may have been translated if We have made them available "
     "to You on our Service. You agree that the original English text shall prevail in the "
     "case of a dispute."),
    ("h2", "Changes to These Terms and Conditions"),
    ("p", "We reserve the right, at Our sole discretion, to modify or replace these Terms at "
     "any time. If a revision is material We will make reasonable efforts to provide at "
     "least 30 days' notice prior to any new terms taking effect. What constitutes a "
     "material change will be determined at Our sole discretion."),
    ("p", "By continuing to access or use Our Service after those revisions become effective, "
     "You agree to be bound by the revised terms. If You do not agree to the new terms, in "
     "whole or in part, please stop using the website and the Service."),
    ("h2", "Contact Us"),
    ("p", "If you have any questions about these Terms and Conditions, You can contact us:"),
    ("p", "By visiting this page on our website: https://pillaiandsons.in/contact.html"),
]

PRIVACY = [
    ("p", "This document outlines the privacy policy of Pillai and Sons Motor Company (referred "
     "to as \"Pillai & Sons\") regarding the information collected during your visits to our "
     "website. The information received depends on how you use the site. These privacy "
     "provisions apply only to Pillai & Sons online information collection activities and "
     "do not apply to information collected outside of this website. By using this site, "
     "you agree to the Pillai & Sons Online Privacy Policy. If you do not agree, please "
     "refrain from using this site. Pillai & Sons reserves the right to change any part of "
     "the Online Privacy Policy without notice."),
    ("h2", "No Representation or Warranty"),
    ("p", "Pillai & Sons cannot guarantee the confidentiality of your use of this site. Pillai "
     "& Sons is not responsible for any harm that may occur as a result of a breach of "
     "confidentiality in relation to your use of this site or any information transmitted "
     "to this site."),
    ("h2", "Normal Website Usage"),
    ("p", "You can visit Pillai & Sons website to read vehicle product information or use our "
     "online tools without providing personal information. During normal website usage, "
     "Pillai & Sons collects and stores information such as the name of your Internet "
     "service provider, browser type, IP address, the website that referred you to us, the "
     "pages you request, and the date and time of those requests. This information is used "
     "to generate statistics and measure site activity to improve customer visits. Pillai "
     "& Sons does not collect or store personally identifiable information such as name, "
     "mailing address, email address, or phone number unless specified in the following "
     "events."),
    ("h2", "Collection of Personally Identifiable Information"),
    ("p", "There are instances where Pillai & Sons requests personally identifiable information "
     "to provide services or correspondence to website visitors (such as new vehicle "
     "information alerts, promotions, and mailed brochures). This information, including "
     "name, mailing address, email address, type of request, and possibly additional "
     "information, is collected and stored by Pillai & Sons to fulfill your request. The "
     "information you provide is used to improve the services provided to you and is never "
     "sold to any other company. Pillai & Sons may share user information with affiliates "
     "and business partners, such as authorized dealers, to provide consistent service, "
     "support, and marketing to existing and prospective customers."),
    ("h2", "Use of Cookies"),
    ("p", "Cookies are used to track site and user activity by transferring information to an "
     "individual's hard drive for record-keeping purposes. Cookies help Pillai & Sons "
     "track popular areas of the site and areas that are not frequently visited, which "
     "aids in improving and updating the site. Most browsers are initially set to accept "
     "cookies, but you can adjust your browser settings to refuse cookies or receive "
     "alerts when cookies are being sent. However, certain parts of the site may not "
     "function properly if cookies are disabled."),
    ("h2", "Third-Party Advertising Company"),
    ("p", "Pillai & Sons may share information about visitors to our website with a reputable "
     "third-party advertising company for the purpose of targeting our internet banner "
     "advertisements on this site and other sites. Pillai & Sons and the third-party "
     "advertising company may track some of the pages you visit through the use of pixel "
     "tags, but this information is not personally identifiable."),
    ("h2", "Legal Terms"),
    ("h2", "Copyright/Trademark Ownership"),
    ("p", "The information on this site is protected by copyright. You may only use the "
     "information, text, or graphics for personal use and must not reproduce, adapt, or "
     "publish it without the express written consent of Pillai & Sons. The names and logos "
     "of Pillai & Sons and Maruti Suzuki, as well as Maruti Suzuki model names, are "
     "trademarks of Pillai & Sons and can only be used with Pillai & Sons permission. The "
     "Pillai & Sons and Maruti Suzuki logos may not be used, downloaded, copied, or "
     "distributed in any way."),
    ("h2", "Limitation on Scope of Content"),
    ("p", "This website contains information about Pillai & Sons and its products and "
     "promotional programs. The Pillai & Sons vehicles described on this site are for sale "
     "only in India and other countries as decided by Pillai & Sons. The promotional "
     "programs mentioned on this site are available only in specific states of India. All "
     "pricing information on this site is in Indian Rupees."),
    ("h2", "No Representation or Warranty"),
    ("p", "Pillai & Sons reserves the right to modify the information on this site without "
     "notice. While Pillai & Sons makes efforts to ensure the accuracy of the material on "
     "this site, accuracy cannot be guaranteed. Pillai & Sons does not assume any "
     "responsibility for the accuracy, completeness, or authenticity of any information on "
     "this site. The site and all information and materials are provided \"as is\" without "
     "warranty of any kind."),
    ("h2", "No Offer to Sell or Lease"),
    ("p", "The information on this site is for informational purposes only and does not "
     "constitute an offer to buy or sell Maruti Suzuki vehicles. The purchase of any "
     "Maruti Suzuki vehicle is subject to the terms and conditions of the applicable sale, "
     "lease, or retail installment contract. The MRP listed on this site does not include "
     "tax, title, license, and registration. Actual dealer price may vary. This site "
     "should not be used as a substitute for information from an authorized Maruti Suzuki "
     "automobile dealer."),
    ("h2", "Hypertext Links to External Sites"),
    ("p", "This site may contain hypertext links to other websites that are independent of this "
     "site. Pillai & Sons does not guarantee the accuracy, completeness, or authenticity "
     "of the information on any linked sites. The inclusion of a hypertext link to another "
     "website should not be construed as an endorsement by Pillai & Sons. Your use of any "
     "off-site pages or other sites linked from this site is at your own risk."),
    ("h2", "Guidelines for External Sites Linking to pillaiandsons.in"),
    ("p", "If you want to link to pillaiandsons.in, please follow these guidelines and comply "
     "with all applicable laws."),
    ("h2", "External Site Naming Guidelines"),
    ("p", "Third parties may not use a brand, product name, or any similar word or group of "
     "letters in a domain name without prior written approval from Pillai & Sons. Domain "
     "names for enthusiast sites should have a “.org” suffix and not create confusion with "
     "the brand names, trademarks, or trade names of Pillai & Sons and Maruti Suzuki."),
    ("h2", "External Site Use of Pillai & Sons Information"),
    ("p", "Prior written approval is required for third-party sites to use any text, "
     "trademarks, graphics, or photographs from Pillai & Sons sources, such as websites or "
     "brochures. Third-party sites may only use brand or model names in their site texts "
     "to describe Maruti Suzuki products. Any other use of Maruti Suzuki brand names, "
     "logos, trademarks, service marks, model names, or service names is strictly "
     "prohibited. Additionally, the use of text or any other material that implies "
     "sponsorship, approval, or affiliation with Pillai & Sons is not allowed."),
    ("h2", "No Misrepresentation"),
    ("p", "Third-party sites must not imply that Pillai & Sons endorses their products or "
     "services. They must not misrepresent their relationship with Pillai & Sons or "
     "provide false information about Pillai & Sons. Third-party sites must also comply "
     "with all relevant laws and regulations and must not infringe upon any intellectual "
     "property or other rights. Content on third-party sites must not be distasteful, "
     "offensive, or controversial."),
    ("h2", "Linking to pillaiandsons.in"),
    ("p", "Third-party sites may not use links to pillaiandsons.in in a way that implies "
     "sponsorship or affiliation. Furthermore, when linking to pillaiandsons.in, the site "
     "containing the link must not appear as a frame within the destination site or in any "
     "way that suggests that the destination site's content belongs to the site containing "
     "the link."),
    ("h2", "External Site Disclaimer"),
    ("p", "Third-party sites must prominently display a disclaimer on their home page stating "
     "that the site is not authorized by or affiliated with Pillai & Sons."),
    ("h2", "Liability Disclaimer"),
    ("p", "The information, software, products, and services on this website may contain "
     "inaccuracies or typographical errors. Pillai & Sons makes no representations about "
     "the suitability, reliability, availability, timeliness, lack of viruses, or accuracy "
     "of the information, software, products, services, and related graphics on the "
     "website. All such information, software, products, services, and graphics are "
     "provided \"as is\" without warranty of any kind. Pillai & Sons disclaims all "
     "warranties and conditions regarding this information, software, products, services, "
     "and graphics, including implied warranties and conditions of merchantability, "
     "fitness for a particular purpose, workmanlike effort, title, and non-infringement. "
     "Pillai & Sons shall not be responsible for unauthorized access or alteration of "
     "transmissions or data, any material or data sent or received, or any transactions "
     "entered into through the Pillai & Sons website. In no event shall Pillai & Sons or "
     "its suppliers be liable for any damages, including without limitation, direct, "
     "indirect, punitive, incidental, special, or consequential damages, or any damages "
     "whatsoever arising out of or in any way connected with the use or performance of the "
     "website/services, the delay or inability to use the website/services, the provision "
     "or failure to provide services, or any information, software, products, services, "
     "and graphics obtained through the website/services, or otherwise arising out of the "
     "use of the website/services, whether based on contract, tort, negligence, strict "
     "liability, or otherwise, even if Pillai & Sons or its suppliers have been advised of "
     "the possibility of damages. If you are dissatisfied with any portion of the "
     "website/services or these terms of use, your sole and exclusive remedy is to "
     "discontinue using the website/services. Pillai & Sons makes no warranty that any "
     "service on this website will be uninterrupted, timely, or secure."),
    ("p", "Pillai & Sons retains the right to disclose any personal information about you or "
     "your use of the Pillai & Sons Site/Services, including its contents, without your "
     "prior permission if Pillai & Sons has a genuine belief that such action is necessary "
     "to: (1) comply with legal requirements or legal processes; (2) safeguard and defend "
     "the rights or property of Pillai & Sons or its affiliated companies; or (3) enforce "
     "the terms of use. Pillai & Sons adherence to this agreement is subject to existing "
     "laws and legal processes, and nothing in this agreement undermines Pillai & Sons "
     "right to comply with governmental, court, and law enforcement requests or "
     "requirements relating to your use of the Pillai & Sons Site/Services or the "
     "information provided to or gathered by Pillai & Sons regarding such use. If any part "
     "of this agreement is found to be invalid or unenforceable according to applicable "
     "law, including the warranty disclaimers and liability limitations mentioned above, "
     "then the invalid or unenforceable provision will be replaced by a valid and "
     "enforceable provision that closely aligns with the original intent, and the "
     "remainder of the agreement will remain in effect."),
    ("h2", "Copyright and Trademark Notices"),
    ("p", "All contents of this website are protected by copyright (c) 2026 Pillai & Sons Motor "
     "Company, 31-A, Medical College Road, Rajjappa Nagar, Jayalakshmi Nagar, Thanjavur, "
     "Tamil Nadu, 613007, India. All rights reserved."),
]

