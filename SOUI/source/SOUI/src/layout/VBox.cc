
#include "souistd.h"
#include "layout/VBox.h"

namespace SOUI
{ 
	 
	SVBox::SVBox()
	{
		m_szView.cx=0;
		m_szView.cy=0;
		m_nEstimateHeight =0;

		m_bClipClient=TRUE;
		GetEventSet()->addEvent(EVENTID(EventScrollViewOriginChanged));
		GetEventSet()->addEvent(EVENTID(EventScrollViewSizeChanged));
		GetEventSet()->addEvent(EVENTID(EventScroll));
	}

	CRect SVBox::GetChildrenLayoutRect()
    {
		 
		bool bShowVerSB=false;
		
		if(m_szView.cx==0)
		{
			if(m_nEstimateHeight> this->GetWindowRect().Height())
				bShowVerSB=true;
		}
		else
		{ 
			if(m_wBarVisible&SSB_VERT)
				bShowVerSB =true;
		}

		int w = this->GetParent()->GetWindowRect().Width();
		
		if(bShowVerSB)
			w -= m_nSbWid; 

		m_szView.cx = w; 

        CRect rcRet=__super::GetChildrenLayoutRect();
        rcRet.OffsetRect(-m_ptOrigin);
        rcRet.right=rcRet.left+m_szView.cx;
        rcRet.bottom=rcRet.top+m_szView.cy;
        return rcRet;
    }

	int SVBox::EstimateViewSize()
	{ 
		int nHeight=0;
		CRect rc;  

		SWindow *pChild = GetWindow(GSW_FIRSTCHILD);
		while(pChild)
		{
			pChild->GetClientRect(&rc);
			nHeight +=rc.Height();
			pChild = pChild->GetWindow(GSW_NEXTSIBLING);
		}

		//CSize oldViewSize(0,0); 	 
		//OnViewSizeChanged(oldViewSize,m_szView);

		return nHeight;
	} 

	void SVBox::OnSize(UINT nType,CSize size)
	{
		__super::OnSize(nType,size);

		
		m_nEstimateHeight = EstimateViewSize();
		m_szView.cy = m_nEstimateHeight;

		int oldBarVisible= m_wBarVisible;
		

		UpdateScrollBar();

		if(oldBarVisible&SSB_VERT && !(m_wBarVisible&SSB_VERT))
		{
			//滚动条去掉了 
			m_szView.cx =0;
			UpdateChildrenPosition();  
		}
		else if(m_wBarVisible&SSB_VERT && !(oldBarVisible&SSB_VERT))
		{
			//滚动条加上了 
			m_szView.cx =0;
			UpdateChildrenPosition();  
		} 
	}

	void SVBox::OnViewOriginChanged( CPoint ptOld,CPoint ptNew )
	{
		UpdateChildrenPosition();
		EventScrollViewOriginChanged evt(this);
		evt.ptOldOrigin = ptOld;
		evt.ptNewOrigin = ptNew;
		FireEvent(evt);
	}

	void SVBox::OnViewSizeChanged( CSize szOld,CSize szNew )
	{
		EventScrollViewSizeChanged evt(this);
		evt.szOldViewSize = szOld;
		evt.szNewViewSize = szNew;
		FireEvent(evt);
	}

	void SVBox::SetViewOrigin(CPoint pt)
	{
		if(m_ptOrigin==pt) return;
		CPoint ptOld=m_ptOrigin;
		m_ptOrigin=pt;
		SetScrollPos(FALSE,m_ptOrigin.x,TRUE);
		SetScrollPos(TRUE,m_ptOrigin.y,TRUE);

		OnViewOriginChanged(ptOld,pt);

		Invalidate();
	}

	CPoint SVBox::GetViewOrigin()
	{
		return m_ptOrigin;
	}


	void SVBox::SetViewSize(CSize szView)
	{
		if(szView==m_szView) return;

		CSize oldViewSize=m_szView;
		m_szView=szView;
		UpdateScrollBar();
		CRect rcClient;
		GetClientRect(&rcClient);
		SSendMessage(WM_SIZE,0,MAKELPARAM(rcClient.Width(),rcClient.Height()));
	    
		OnViewSizeChanged(oldViewSize,szView);
	}

	CSize SVBox::GetViewSize()
	{
		return m_szView;
	}

	void SVBox::UpdateScrollBar()
	{
		CRect rcClient;
		SWindow::GetClientRect(&rcClient);

		CSize size=rcClient.Size();
		m_wBarVisible=SSB_NULL;    //关闭滚动条

		if(size.cy<m_szView.cy || (size.cy<m_szView.cy+m_nSbWid && size.cx<m_szView.cx))
		{
			//需要纵向滚动条
			m_wBarVisible|=SSB_VERT;
			m_siVer.nMin=0;
			m_siVer.nMax=m_szView.cy-1;
			m_siVer.nPage=size.cy;

			if(size.cx<m_szView.cx)//+m_nSbWid)
			{
				//需要横向滚动条
				m_wBarVisible |= SSB_HORZ;
				m_siVer.nPage=size.cy-m_nSbWid > 0 ? size.cy-m_nSbWid : 0;

				m_siHoz.nMin=0;
				m_siHoz.nMax=m_szView.cx-1;
				m_siHoz.nPage=size.cx-m_nSbWid > 0 ? size.cx-m_nSbWid : 0;
			}
			else
			{
				//不需要横向滚动条
				m_siHoz.nPage=size.cx;
				m_siHoz.nMin=0;
				m_siHoz.nMax=m_siHoz.nPage-1;
				m_siHoz.nPos=0;
				m_ptOrigin.x=0;
			}
		}
		else
		{
			//不需要纵向滚动条
			m_siVer.nPage=size.cy;
			m_siVer.nMin=0;
			m_siVer.nMax=size.cy-1;
			m_siVer.nPos=0;
			m_ptOrigin.y=0;

			if(size.cx<m_szView.cx)
			{
				//需要横向滚动条
				m_wBarVisible|=SSB_HORZ;
				m_siHoz.nMin=0;
				m_siHoz.nMax=m_szView.cx-1;
				m_siHoz.nPage=size.cx;
			}
			//不需要横向滚动条
			else
			{
				m_siHoz.nPage=size.cx;
				m_siHoz.nMin=0;
				m_siHoz.nMax=m_siHoz.nPage-1;
				m_siHoz.nPos=0;
				m_ptOrigin.x=0;
			}
		}

		SetScrollPos(TRUE,m_siVer.nPos,TRUE);
		SetScrollPos(FALSE,m_siHoz.nPos,TRUE);

		SSendMessage(WM_NCCALCSIZE);

		Invalidate();
	}

	BOOL SVBox::OnScroll(BOOL bVertical,UINT uCode,int nPos)
	{
		BOOL bRet=__super::OnScroll(bVertical,uCode,nPos);
		if(bRet)
		{
			int nPos=GetScrollPos(bVertical);
			CPoint ptOrigin=m_ptOrigin;

			if(bVertical) ptOrigin.y=nPos;
			else ptOrigin.x=nPos;

			if(ptOrigin!=m_ptOrigin)
				SetViewOrigin(ptOrigin);

			if(uCode==SB_THUMBTRACK)
				ScrollUpdate();
	            
			EventScroll evt(this);
			evt.bVertical = bVertical;
			evt.uSbCode = uCode;
			evt.nPos = nPos;
			FireEvent(evt);
		}
		return bRet;
	}


}