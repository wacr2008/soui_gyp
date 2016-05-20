
#include "souistd.h"
#include "layout/HBox.h"

namespace SOUI
{ 
	 
	SHBox::SHBox()
	{
		m_szView.cx=0;
		m_szView.cy=0;
		m_nEstimateWidth =0;

		m_bClipClient=TRUE;
		GetEventSet()->addEvent(EVENTID(EventScrollViewOriginChanged));
		GetEventSet()->addEvent(EVENTID(EventScrollViewSizeChanged));
		GetEventSet()->addEvent(EVENTID(EventScroll));
	}

	CRect SHBox::GetChildrenLayoutRect()
    {
		 
		bool bShowHorSB=false;
		
		if(m_szView.cy==0)
		{
			if(m_nEstimateWidth> this->GetWindowRect().Width())
				bShowHorSB=true;
		}
		else
		{ 
			if(m_wBarVisible&SSB_HORZ)
				bShowHorSB =true;
		}

		int h = this->GetParent()->GetWindowRect().Height();
		
		if(bShowHorSB)
			h -= m_nSbWid; 

		m_szView.cy = h; 

        CRect rcRet=__super::GetChildrenLayoutRect();
        rcRet.OffsetRect(-m_ptOrigin);
        rcRet.right=rcRet.left+m_szView.cx;
        rcRet.bottom=rcRet.top+m_szView.cy;
        return rcRet;
    }

	int SHBox::EstimateViewSize()
	{ 
		int nWidth=0;
		CRect rc;  

		SWindow *pChild = GetWindow(GSW_FIRSTCHILD);
		while(pChild)
		{
			pChild->GetClientRect(&rc);
			nWidth +=rc.Width();
			pChild = pChild->GetWindow(GSW_NEXTSIBLING);
		}

		//CSize oldViewSize(0,0); 	 
		//OnViewSizeChanged(oldViewSize,m_szView);

		return nWidth;
	} 

	void SHBox::OnSize(UINT nType,CSize size)
	{
		__super::OnSize(nType,size);

		
		m_nEstimateWidth = EstimateViewSize();
		m_szView.cx = m_nEstimateWidth;

		int oldBarVisible= m_wBarVisible;
		

		UpdateScrollBar();

		if(oldBarVisible&SSB_HORZ && !(m_wBarVisible&SSB_HORZ))
		{
			//滚动条去掉了 
			m_szView.cy =0;
			UpdateChildrenPosition();  
		}
		else if(m_wBarVisible&SSB_HORZ && !(oldBarVisible&SSB_HORZ))
		{
			//滚动条加上了 
			m_szView.cy =0;
			UpdateChildrenPosition();  
		} 
	}

	void SHBox::OnViewOriginChanged( CPoint ptOld,CPoint ptNew )
	{
		UpdateChildrenPosition();
		EventScrollViewOriginChanged evt(this);
		evt.ptOldOrigin = ptOld;
		evt.ptNewOrigin = ptNew;
		FireEvent(evt);
	}

	void SHBox::OnViewSizeChanged( CSize szOld,CSize szNew )
	{
		EventScrollViewSizeChanged evt(this);
		evt.szOldViewSize = szOld;
		evt.szNewViewSize = szNew;
		FireEvent(evt);
	}

	void SHBox::SetViewOrigin(CPoint pt)
	{
		if(m_ptOrigin==pt) return;
		CPoint ptOld=m_ptOrigin;
		m_ptOrigin=pt;
		SetScrollPos(FALSE,m_ptOrigin.x,TRUE);
		SetScrollPos(TRUE,m_ptOrigin.y,TRUE);

		OnViewOriginChanged(ptOld,pt);

		Invalidate();
	}

	CPoint SHBox::GetViewOrigin()
	{
		return m_ptOrigin;
	}


	void SHBox::SetViewSize(CSize szView)
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

	CSize SHBox::GetViewSize()
	{
		return m_szView;
	}

	void SHBox::UpdateScrollBar()
	{
		CRect rcClient;
		SWindow::GetClientRect(&rcClient);

		CSize size=rcClient.Size();
		m_wBarVisible=SSB_NULL;    //关闭滚动条

		//if(size.cy<m_szView.cy || (size.cy<m_szView.cy+m_nSbWid && size.cx<m_szView.cx))
		if(size.cy<m_szView.cy || (size.cy<m_szView.cy && size.cx<m_szView.cx))
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

	BOOL SHBox::OnScroll(BOOL bVertical,UINT uCode,int nPos)
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